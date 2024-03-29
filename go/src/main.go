package main

import (
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/dominickp/glue/go/src/handler"
	"github.com/dominickp/glue/go/src/metrics"
	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// https://techwasti.com/cors-handling-in-go-gin-framework
func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "*")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "*")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	}
}

// metricsMiddleware captures the request time and the response code in Prometheus metrics.
func metricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Next()
		elapsed := time.Since(start)
		// Get the normalized route like "/user/:id" 
		normalizedPath := c.FullPath()
		if normalizedPath == "" {
			normalizedPath = "not_found"
		}
		// Capture the request time in milliseconds
		metrics.MetricTotalRequestTime.WithLabelValues(
			c.Request.Method,
			normalizedPath, 
			fmt.Sprintf("%d", c.Writer.Status()),
		).Observe(float64(elapsed.Milliseconds()))
	}
}

// validateCurlRequestMiddleware is a middleware that checks if the request is made using curl.
// If the request is not made using curl, it returns a HTML response with an error message.
func validateCurlRequestMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		if c.Request.URL.Path != "/metrics" && !strings.HasPrefix(c.GetHeader("User-Agent"), "curl") {
			requestURL := c.Request.Host + c.Request.URL.String() // "localhost:8002/"
			c.Data(http.StatusBadRequest, "text/html; charset=utf-8",
				[]byte(fmt.Sprintf(`
					<html>
						<div>
							<p>This API returns text-based responses intended to be used with curl.</p>
							<p>Try "curl %s".</p>
						</div>
					</html>`, requestURL),
				),
			)
			c.Abort()
			return
		}
	}
}

func main() {

	r := gin.Default()
	r.Use(corsMiddleware())
	r.Use(validateCurlRequestMiddleware())
	r.Use(metricsMiddleware())
	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "You should call /<board>/<page> to get the catalog of a board.\n")
	})
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))
	r.GET("/:name", handler.HandleCatalog)
	r.GET("/:name/:page", handler.HandleCatalog)
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	r.Run("0.0.0.0:80")
}
