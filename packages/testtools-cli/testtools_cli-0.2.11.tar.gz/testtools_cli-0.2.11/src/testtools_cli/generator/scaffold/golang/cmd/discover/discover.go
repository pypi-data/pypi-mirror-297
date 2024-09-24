package discover

import (
	"replace_____me/pkg/testcase"
	"replace_____me/pkg/util"

	"github.com/OpenTestSolar/testtool-sdk-golang/client"
	"github.com/OpenTestSolar/testtool-sdk-golang/model"
	"github.com/pkg/errors"
	"github.com/spf13/cobra"
)

type DiscoverOptions struct {
	discoverPath string
}

// NewDiscoverOptions NewBuildOptions new build options with default value
func NewDiscoverOptions() *DiscoverOptions {
	return &DiscoverOptions{}
}

// NewCmdDiscover NewCmdBuild create a build command
func NewCmdDiscover() *cobra.Command {
	o := NewDiscoverOptions()
	cmd := cobra.Command{
		Use:   "discover",
		Short: "Discover testcases",
		RunE: func(cmd *cobra.Command, args []string) error {
			return o.RunDiscover(cmd)
		},
	}
	cmd.Flags().StringVarP(&o.discoverPath, "path", "p", "", "Path of testcase info")
	_ = cmd.MarkFlagRequired("path")
	return &cmd
}

func reportTestcases(fileReportPath string, testcases []*testcase.TestCase, loadErrors []*model.LoadError) error {
	var tests []*model.TestCase

	reporter, err := client.NewReporterClient(fileReportPath)
	if err != nil {
		return errors.Wrapf(err, "failed to create reporter")
	}
	for _, testcase := range testcases {
		tests = append(tests, &model.TestCase{
			Name:       testcase.GetSelector(),
			Attributes: testcase.Attributes,
		})
	}
	err = reporter.ReportLoadResult(&model.LoadResult{
		Tests:      tests,
		LoadErrors: loadErrors,
	})
	if err != nil {
		return errors.Wrap(err, "failed to report load result")
	}
	return nil
}

func (o *DiscoverOptions) RunDiscover(cmd *cobra.Command) error {
	var testcases []*testcase.TestCase
	var loadErrors []*model.LoadError

	// config.ProjectPath: test case repository root directory
	// config.TestSelectors: list of test cases expected to be loaded
	// config.TaskId: the identifier of this task
	config, err := util.UnmarshalCaseInfo(o.discoverPath)
	if err != nil {
		return errors.Wrapf(err, "failed to unmarshal case info")
	}
	// TODO: load test cases based on configuration information `config`
	// Test cases for both successful and failed loads are returned in the form of slices
	// represented by testcase.TestCase and model.LoadError, respectively

	err = reportTestcases(config.FileReportPath, testcases, loadErrors)
	if err != nil {
		return errors.Wrapf(err, "failed to report testcases")
	}
	return nil
}
