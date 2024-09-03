$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: 'get3D',
        success: function (data) {
            let obj5 = JSON.parse(data);
            if (obj5.status == 201) {
                console.error(obj5); // 使用 console.error 代替 this.error
                return;
            }

            var d = new Date(), str = '';
            str += d.getFullYear() + '年';
            str += d.getMonth() + 1 + '月';

            // 提取地域和薪资
            const regions = [...new Set(obj5.data.map(item => item.province))];

            // 构建3D柱状图所需的数据格式
            const seriesData = [{
                name: '平均工资',
                data: regions.map(region => {
                    const regionData = obj5.data.find(item => item.province === region);
                    return {
                        x: regions.indexOf(region),
                        y: regionData ? regionData.average_salary : 0
                    };
                })
            }];

            // 创建3D柱状图
            let chart = Highcharts.chart('3Dchart-container', {
                chart: {
                    type: 'column',
                    options3d: {
                        enabled: true,
                        alpha: 10,
                        beta: 30,
                        depth: 100,
                        viewDistance: 25
                    },
                    backgroundColor: 'rgba(0,0,0,0)'
                //     events: {
                //         // 监听滚轮事件以实现缩放
                //         load: function() {
                //             const container = this.container;
                //             const offset = $(container).offset();
                //
                //             $(container).on('wheel', function(event) {
                //                 event.preventDefault();
                //
                //                 const deltaY = event.originalEvent.deltaY;
                //                 const zoomFactor = 0.1; // 缩放因子
                //                 const zoomAmount = deltaY > 0 ? -zoomFactor : zoomFactor;
                //
                //                 // 计算缩放区域
                //                 const xAxis = chart.xAxis[0];
                //                 const yAxis = chart.yAxis[0];
                //                 const xMin = xAxis.min + (xAxis.max - xAxis.min) * zoomAmount;
                //                 const xMax = xAxis.max - (xAxis.max - xAxis.min) * zoomAmount;
                //                 const yMin = yAxis.min + (yAxis.max - yAxis.min) * zoomAmount;
                //                 const yMax = yAxis.max - (yAxis.max - yAxis.min) * zoomAmount;
                //
                //                 // 应用缩放
                //                 chart.zoom({
                //                     xAxis: {
                //                         min: xMin,
                //                         max: xMax
                //                     },
                //                     yAxis: {
                //                         min: yMin,
                //                         max: yMax
                //                     }
                //                 });
                //             });
                //         }
                //     }
                // },
                },
                title: {
                    text: '地域与薪资之间的关系'
                },
                subtitle: {
                    text: '数据截止 ' + str + '，来源: <a href="https://zhipin.com">Boss直聘</a>'
                },
                xAxis: {
                    categories: regions,
                    title: {
                        text: '地域'
                    },
                    labels: {
                        skew3d: true,
                        rotation: -45
                    }
                },
                yAxis: {
                    title: {
                        text: '薪资'
                    },
                    min: 0
                },
                zAxis: {
                    enabled: false // 移除 zAxis，因为我们不再使用
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '地域: {point.category}<br>平均工资: {point.y} K'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: seriesData,
                plotOptions: {
                    column: {
                        depth: 25
                    }
                }
            });

            // 添加鼠标和触控事件来旋转图表
            (function (H) {
                function dragStart(eStart) {
                    eStart = chart.pointer.normalize(eStart);

                    const posX = eStart.chartX,
                        posY = eStart.chartY,
                        alpha = chart.options.chart.options3d.alpha,
                        beta = chart.options.chart.options3d.beta,
                        sensitivity = 5,  // lower is more sensitive
                        handlers = [];

                    function drag(e) {
                        // Get e.chartX and e.chartY
                        e = chart.pointer.normalize(e);

                        chart.update({
                            chart: {
                                options3d: {
                                    alpha: alpha + (e.chartY - posY) / sensitivity,
                                    beta: beta + (posX - e.chartX) / sensitivity
                                }
                            }
                        }, undefined, undefined, false);
                    }

                    function unbindAll() {
                        handlers.forEach(function (unbind) {
                            if (unbind) {
                                unbind();
                            }
                        });
                        handlers.length = 0;
                    }

                    handlers.push(H.addEvent(document, 'mousemove', drag));
                    handlers.push(H.addEvent(document, 'touchmove', drag));
                    handlers.push(H.addEvent(document, 'mouseup', unbindAll));
                    handlers.push(H.addEvent(document, 'touchend', unbindAll));
                }
                H.addEvent(chart.container, 'mousedown', dragStart);
                H.addEvent(chart.container, 'touchstart', dragStart);
            }(Highcharts));
        },
        error: function (xhr, type, errorThrown) {
            console.error("Error: " + errorThrown); // 错误处理
        }
    });
});
