package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (

	msBuckets = []float64{
		5, 10, 25, 50, 75, 100, 125 ,150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 600, 
		700, 800, 900, 1000, 2000, 3000, 4000, 5000,
	}

	MetricTotalRequestTime = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "total_request_seconds",
			Help:    "Total time taken to process a request",
			Buckets: msBuckets,
			ConstLabels: map[string]string{"app": "glue-go"},
		},
		[]string{"method", "endpoint", "response_code"},
	)

	MetricFanoutRequestTime = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "fanout_request_seconds",
			Help:    "Time taken to fanout to all the services",
			Buckets: msBuckets,
			ConstLabels: map[string]string{"app": "glue-go"},
		},
		[]string{"method", "endpoint", "response_code"},
	)

	MetricChanBoardsRequested = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "chan_boards_requested",
            Help: "Number of times a 4channel board was requested",
			ConstLabels: map[string]string{"app": "glue-go"},
        },
        []string{"board"},
    )
)
