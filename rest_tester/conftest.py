"""
This file is the starting point of pytest package
"""

from base64 import b64decode

import pytest
from pytest_html import extras

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix):
    """
    Adds a custom HTML summary to the pytest HTML report. The summary includes a pie chart showing the test outcomes.
    
    :param prefix: A list of HTML elements to be added to the report summary.
    :type prefix: list
    
    :return: None
    :rtype: None
    """
    prefix.extend([extras.html("""
        <script>
          document.addEventListener('DOMContentLoaded', function() {
            var event = new CustomEvent('reportRendered');
            document.dispatchEvent(event);
        });
        </script>                               
        <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>
            <div class="chart-container">
                <canvas id="outcomeChart"></canvas>
            </div>
    <script>
    document.addEventListener('reportRendered', function() {
    function getTestResults() {
        var results = {
            passed: 0,
            failed: 0,
            skipped: 0,
            xfailed: 0,
            xpassed: 0,
            error: 0,
            rerun: 0
        };

        // Query the summary elements for test counts
        var summaryElements = document.querySelectorAll('.summary__data .controls .filters span');
        summaryElements.forEach(function(element) {
            var textContent = element.textContent;
            var match = textContent.match(/(\d+)\s+(\w+)/);
            if (match) {
                var count = parseInt(match[1], 10);
                var key = match[2].toLowerCase();
                if (key in results) {
                    results[key] = count;
                }
            }
        });

        return results;
    }

    // Get the test results
    var testResults = getTestResults();

    // Prepare the data for the pie chart
    var data = {
        labels: [],
        datasets: [{
            data: [],
            backgroundColor: [],
            hoverBackgroundColor: []
        }]
    };

    // Define colors for the chart
    var colors = {
        'passed': '#5cb85c',
        'failed': '#d9534f',
        'skipped': '#f0ad4e',
        'xfailed': '#5bc0de',
        'xpassed': '#5bc0de',
        'error': '#d9534f',
        'rerun': '#777'
    };

    // Populate the data object with values from the outcomes
    Object.keys(testResults).forEach(function(result) {
        if (testResults[result] > 0) {
            data.labels.push(result.charAt(0).toUpperCase() + result.slice(1));
            data.datasets[0].data.push(testResults[result]);
            data.datasets[0].backgroundColor.push(colors[result]);
            data.datasets[0].hoverBackgroundColor.push(colors[result]);
        }
    });

    // Calculate the total test count
    var totalTestCount = Object.values(testResults).reduce(function(total, count) {
        return total + count;
    }, 0);

    // Plugin to display text in the center of the donut chart
    Chart.pluginService.register({
        beforeDraw: function(chart) {
        if (chart.config.options.elements.center) {
            // Get ctx from string
            var ctx = chart.chart.ctx;
            
            // Get options from the center object in options
            var centerConfig = chart.config.options.elements.center;
            var fontStyle = centerConfig.fontStyle || 'Arial';
            var txt = centerConfig.text || '';
            var color = centerConfig.color || '#000';
            var sidePadding = centerConfig.sidePadding || 20;
            var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2);
            // Start with a base font of 30px
            ctx.font = "60px " + fontStyle;
            
            // Get the width of the string and also the width of the element minus 10 to give it 5px side padding
            var stringWidth = ctx.measureText(txt).width;
            var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

            // Find out how much the font can grow in width.
            var widthRatio = elementWidth / stringWidth;
            var newFontSize = Math.floor(30 * widthRatio);
            var elementHeight = (chart.innerRadius * 2);

            // Pick a new font size so it will not be larger than the height of label.
            var fontSizeToUse = Math.min(newFontSize, elementHeight);

            // Set font settings to draw it correctly.
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
            var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
            ctx.font = fontSizeToUse + "px " + fontStyle;
            ctx.fillStyle = color;

            // Draw text in center
            ctx.fillText(txt, centerX, centerY);
        }
        }
    });

    // Render the donut chart
    var ctx = document.getElementById('outcomeChart').getContext('2d');
    var outcomeChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            position: 'right',
            labels: {
            fontColor: '#ffffff'
            }
        },
        title: {
            display: true,
            text: 'Test Outcomes',
            fontColor: '#ffffff'
        },
        animation: {
            animateScale: true,
            animateRotate: true
        },
        cutoutPercentage: 60,
        elements: {
            center: {
            text: totalTestCount.toString(), // Text to display in center
            color: '#ffffff', // Text color
            fontStyle: 'Arial', // Font style
            sidePadding: 20 // Padding around text
            }
        }
        }
    });});
    </script>                               
        """)['content']])

def pytest_html_results_table_header(cells):
    """
    Takes a list of cells and modifies it by filtering out cells containing 'Links', moving the testId cell to the beginning, and inserting 'Test Type', 'Expected', and 'Actual' headers.
    """
    cells[:] = [cell for cell in cells if 'Links' not in cell]
    test_index = next(i for i, cell in enumerate(cells) if 'data-column-type="testId"' in cell)
    cells.insert(0, cells.pop(test_index))
    cells.insert(1, '<th>Test Type</th>')
    cells.insert(2, '<th>Expected</th>')
    cells.insert(3, '<th>Actual</th>') 

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This function is a pytest hook implementation that is called when a test is executed. It modifies the test report by adding extra information to the report's 'extras' attribute.

    Parameters:
    - item: The test item being executed.
    - call: The test call being executed.

    Returns:
    - None
    """
    outcome = yield
    report = outcome.get_result()
    report.extras = getattr(report, "extras", [])

    if report.when == "call":

        type_col = item.get_closest_marker("test_type")
        expected_col = item.get_closest_marker("expected")
        actual_col = item.get_closest_marker("actual")

        if type_col:
            report.extras.append(extras.text(type_col.args[0], name='Test Type'))
        if expected_col:
            report.extras.append(extras.text(expected_col.args[0], name='Expected'))
        if actual_col:
            report.extras.append(extras.text(actual_col.args[0], name='Actual'))

def pytest_html_results_table_row(report, cells):
    """
    Takes a report object and a list of cells, modifies the list of cells by filtering out cells containing 'class="col-links"', moving the cell containing 'class="col-testId"' to the beginning, and inserting cells with the values of 'Test Type', 'Expected', and 'Actual'.

    :param report: A pytest report object.
    :type report: pytest.Report
    :param cells: A list of HTML cells representing the columns of a test results table.
    :type cells: List[str]
    :return: None
    """
    extra = getattr(report, 'extras', [])
    type_col = next((x for x in extra if x.get('name') == 'Test Type'), {}).get('content', 'N/A')
    expected_col = next((x for x in extra if x.get('name') == 'Expected'), {}).get('content', 'N/A')
    actual_col = next((x for x in extra if x.get('name') == 'Actual'), {}).get('content', 'N/A')

    type_col = b64decode(type_col.split(",")[1]).decode('utf-8') if type_col.startswith('data:') else type_col
    expected_col = b64decode(expected_col.split(",")[1]).decode('utf-8') if expected_col.startswith('data:') else expected_col
    actual_col = b64decode(actual_col.split(",")[1]).decode('utf-8') if actual_col.startswith('data:') else actual_col

    cells[:] = [cell for cell in cells if 'class="col-links"' not in cell]
    test_index = next(i for i, cell in enumerate(cells) if 'class="col-testId"' in cell)
    cells.insert(0, cells.pop(test_index).replace('rest_tester/main.py::test_api[', '').replace(f' - {type_col}]',''))
    cells.insert(1, f'<td>{type_col}</td>')
    cells.insert(2, f'<td>{expected_col}</td>')
    cells.insert(3, f'<td>{actual_col}</td>')                  
