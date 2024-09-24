package execute

import (
	"replace_____me/pkg/util"

	"github.com/OpenTestSolar/testtool-sdk-golang/client"
	"github.com/OpenTestSolar/testtool-sdk-golang/model"
	"github.com/pkg/errors"
	"github.com/spf13/cobra"
)

type ExecuteOptions struct {
	executePath string
}

// NewExecuteOptions NewBuildOptions new build options with default value
func NewExecuteOptions() *ExecuteOptions {
	return &ExecuteOptions{}
}

// NewCmdExecute NewCmdBuild create a build command
func NewCmdExecute() *cobra.Command {
	o := NewExecuteOptions()
	cmd := cobra.Command{
		Use:   "execute",
		Short: "Execute testcases",
		RunE: func(cmd *cobra.Command, args []string) error {
			return o.RunExecute(cmd)
		},
	}
	cmd.Flags().StringVarP(&o.executePath, "path", "p", "", "Path of testcase info")
	_ = cmd.MarkFlagRequired("path")
	return &cmd
}

func reportTestResults(fileReportPath string, testResults []*model.TestResult) error {
	reporter, err := client.NewReporterClient(fileReportPath)
	if err != nil {
		return errors.Wrap(err, "failed to create reporter")
	}
	for _, result := range testResults {
		err := reporter.ReportCaseResult(result)
		if err != nil {
			return errors.Wrap(err, "failed to report load result")
		}
	}
	return nil
}

func (o *ExecuteOptions) RunExecute(cmd *cobra.Command) error {
	var testResults []*model.TestResult

	// config.ProjectPath: test case repository root directory
	// config.TestSelectors: list of test cases expected to be executed
	// config.TaskId: the identifier of this task
	config, err := util.UnmarshalCaseInfo(o.executePath)
	if err != nil {
		return errors.Wrapf(err, "failed to pasrse case info")
	}
	// TODO: execute test cases based on configuration information `config`
	// The results of the executed test cases are returned in the form of slices and represented by model.TestResult.

	err = reportTestResults(config.FileReportPath, testResults)
	if err != nil {
		return errors.Wrapf(err, "failed to report test results")
	}
	return nil
}
