package internal

import (
	"errors"
	"fmt"
	"io"
	"io/fs"
	"log"
	"os"
	"path/filepath"
	"slices"

	"github.com/tidwall/gjson"

	"golang.org/x/term"

	"github.com/urfave/cli/v2"

	"github.com/ossf/osv-schema/linter/internal/checks"
)

type Content struct {
	filename string
	bytes    []byte
}

type LintConfig struct {
	verbose bool
}

func lint(content *Content, checksDefined []*checks.CheckDef, config *LintConfig) (findings []checks.CheckError) {
	// Parse file into JSON
	if !gjson.ValidBytes(content.bytes) {
		log.Printf("%q: invalid JSON", content.filename)
	}

	record := gjson.ParseBytes(content.bytes)

	for _, check := range checksDefined {
		if config.verbose {
			fmt.Printf("Running %q check on %q\n", check.Name, content.filename)
		}
		checkConfig := checks.Config{Verbose: config.verbose}
		checkFindings := check.Run(&record, &checkConfig)
		if checkFindings != nil && config.verbose {
			log.Printf("%q: %q: %#v", content.filename, check.Name, checkFindings)
		}
		findings = append(findings, checkFindings...)
	}
	return findings
}

func LintCommand(cCtx *cli.Context) error {
	// List check collections.
	if cCtx.String("collection") == "list" {
		fmt.Printf("Available check collections:\n\n")
		for _, collection := range checks.Collections {
			fmt.Printf("%s: %s\n", collection.Name, collection.Description)
			for _, check := range collection.Checks {
				fmt.Printf("\t%s: (%s): %s\n", check.Code, check.Name, check.Description)
			}
		}
		return nil
	}

	// List all available checks.
	if slices.Contains(cCtx.StringSlice("check"), "list") {
		fmt.Printf("Available checks:\n\n")
		for _, check := range checks.CollectionFromName("ALL").Checks {
			fmt.Printf("%s: (%s): %s\n", check.Code, check.Name, check.Description)
		}
		return nil
	}

	// Check for things to check.
	if !cCtx.Args().Present() && term.IsTerminal(int(os.Stdin.Fd())) {
		return errors.New("no files to check (use - for stdin)")
	}

	var checksToBeRun []*checks.CheckDef

	// Run just individual checks.
	for _, checkRequested := range cCtx.StringSlice("check") {
		// Check the requested check exists.
		check := checks.FromCode(checkRequested)
		if check == nil {
			return fmt.Errorf("%q is not a valid check", checkRequested)
		}
		checksToBeRun = append(checksToBeRun, check)
	}

	// Run all the checks in a collection, if no specific checks requested.
	if checksToBeRun == nil && cCtx.String("collection") != "" {
		if cCtx.Bool("verbose") {
			if cCtx.Args().Present() {
				fmt.Printf("Running %q check collection on %q\n", cCtx.String("collection"), cCtx.Args())
			} else {
				fmt.Printf("Running %q check collection on <stdin>\n", cCtx.String("collection"))
			}
		}
		// Check the requested check collection exists.
		collection := checks.CollectionFromName(cCtx.String("collection"))
		if collection == nil {
			return fmt.Errorf("%q is not a valid check collection", cCtx.String("collection"))
		}
		checksToBeRun = collection.Checks
	}

	perFileFindings := map[string][]checks.CheckError{}

	// Figure out what files to check.
	var filesToCheck []string
	for _, thingToCheck := range cCtx.Args().Slice() {
		// Special case "-" for stdin.
		if thingToCheck == "-" {
			filesToCheck = append(filesToCheck, "<stdin>")
			continue
		}

		file, err := os.Open(thingToCheck)
		if err != nil {
			log.Printf("%v, skipping", err)
			continue
		}
		defer file.Close()

		fileInfo, err := file.Stat()
		if err != nil {
			log.Printf("%v, skipping", err)
			continue
		}

		if fileInfo.IsDir() {
			err := filepath.WalkDir(thingToCheck, func(f string, d fs.DirEntry, err error) error {
				if err != nil {
					return err
				}
				if !d.IsDir() && filepath.Ext(d.Name()) == ".json" {
					filesToCheck = append(filesToCheck, f)
				}
				return nil
			})
			if err != nil {
				log.Printf("%v, skipping", err)
				continue
			}
			if cCtx.Bool("verbose") {
				log.Printf("Found %d files in %q", len(filesToCheck), thingToCheck)
			}
		} else {
			filesToCheck = append(filesToCheck, thingToCheck)
		}
	}

	// Default to stdin if no files were specified.
	if len(filesToCheck) == 0 {
		filesToCheck = append(filesToCheck, "<stdin>")
	}

	// Run the check(s) on the files.
	for _, fileToCheck := range filesToCheck {
		var recordBytes []byte
		var err error
		// Special case for stdin.
		if fileToCheck == "<stdin>" {
			recordBytes, err = io.ReadAll(os.Stdin)
		} else {
			recordBytes, err = os.ReadFile(fileToCheck)
		}
		if err != nil {
			log.Printf("%v, skipping", err)
			continue
		}
		findings := lint(&Content{filename: fileToCheck, bytes: recordBytes}, checksToBeRun, &LintConfig{verbose: cCtx.Bool("verbose")})
		if findings != nil {
			perFileFindings[fileToCheck] = findings
		}
	}

	if len(perFileFindings) > 0 {
		for filename, findings := range perFileFindings {
			fmt.Printf("%s:\n", filename)
			for _, finding := range findings {
				fmt.Printf("\t * %s\n", finding.Error())
			}
		}
		return errors.New("found errors")
	}
	return nil
}
