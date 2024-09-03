$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: 'getline',
        success: function (data) {
            let obj4 = JSON.parse(data)
            if (obj4.status == 201) {
                this.error(xhr = obj4)
                return
            }
            var d = new Date(),str = '';
             str += d.getFullYear() + '年'; //获取当前年份
				str += d.getMonth() + 1 + '月'; //获取当前月份（0——11）
            const categories = obj4.data.map(item => item.education_level);
            const salary = obj4.data.map(item => item.average_salary);
            let chart=Highcharts.chart('linechart-container', {
                chart: {
                type: 'line',  // Specifies the type of chart as a line chart
                backgroundColor: 'rgba(0,0,0,0)'  // Optional: sets background color
                },
                title: {
                    text: '工资与学历之间的联系'  // Title of the chart
                },
                subtitle: {
                    text: '数据截止 '+str+'，来源: <a href="https://zhipin.com">Boss直聘</a>' // Optional: subtitle of the chart
                },
                xAxis: {
                    type: 'category',
                    categories:categories,
                    labels: {
                        rotation: -45  // 设置轴标签旋转角度
                    }
                },
                yAxis: {
                    title: {
                        text: '工资'  // Title of the y-axis
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'  // Optional: line across the y-axis
                    }]
                },
                tooltip: {
                    valueSuffix: ' K'  // Optional: suffix for tooltip values
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name:'工资',
                    data:salary,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#FFFFFF',
                        align: 'right',
                        format: '{point.y}', // :.1f 为保留 1 位小数
                        y: 10
                    }
                }]
            })
        },
        error: function (xhr, type, errorThrown) {
            alert(xhr.data)
        }
    })
})