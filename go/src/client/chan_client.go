package client

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/dominickp/glue/go/src/metrics"

	"github.com/go-resty/resty/v2"
)

const (
	defaultChanHost = "https://a.4cdn.org"
)

var (
	restyClient             *resty.Client
	host                    string
	sfwSupportedBoardsArray = [...]string{"po", "g", "fa", "mu", "v"}
)

// getEnvString returns the value of the environment variable named by the key,
// or fallback if the environment variable is not set.
func getEnvString(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func init() {
	host = getEnvString("CHAN_HOST", defaultChanHost)
	restyClient = resty.New().
		SetJSONMarshaler(json.Marshal).
		SetJSONUnmarshaler(json.Unmarshal).
		SetTimeout(time.Duration(5) * time.Second) // Set timeout to 5 seconds
}

// handleRequest is a helper function that handles the request to the 4channel API and captures fanout metrics.
func handleRequest(method string, endpoint string, headers map[string]string, result interface{}) error {
	start := time.Now()

	response, err := restyClient.R().
		SetHeaders(headers).
		SetResult(result).
		Get(host + endpoint)
	if err != nil {
		return err
	}
	if response.IsError() {
		return errors.New(fmt.Sprintf("Error: %s", response.String()))
	}

	// Capture the request time in milliseconds
	elapsed := time.Since(start)
	metrics.MetricFanoutRequestTime.WithLabelValues(
		method, 
		host + endpoint, 
		fmt.Sprintf("%d", response.StatusCode(),
		),
	).Observe(float64(elapsed.Milliseconds()))
	
	return nil
}

// GetCatalog retrieves the catalog of a supported SFW board.
// The 'board' parameter specifies the board to get the catalog of (e.g., "po" for Papercraft & Origami).
// The 'headers' parameter specifies any optional headers to be sent in the request.
func GetCatalog(board string, headers map[string]string) ([]CatalogPage, error) {

	// Check if the board is in the sfwSupportedBoardsArray
	isSupported := false
	for _, supportedBoard := range sfwSupportedBoardsArray {
		if board == supportedBoard {
			isSupported = true
			break
		}
	}
	if !isSupported {
		return nil, errors.New(fmt.Sprintf("Board %s is not a supported SFW board.", board))
	}

	// Capture the 4channel board metric now that we know the value is of a small set.
	metrics.MetricChanBoardsRequested.WithLabelValues(board).Inc()

	// Call the 4channel API to get the catalog
	catalogResponse := []CatalogPage{}
	err := handleRequest("GET", fmt.Sprintf("/%s/catalog.json", board), headers, &catalogResponse)
	if err != nil {
		return nil, err
	}

	return catalogResponse, nil
}
