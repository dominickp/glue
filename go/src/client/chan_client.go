package client

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"time"

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

	// Call the 4channel API to get the catalog
	catalogResponse := []CatalogPage{}
	response, err := restyClient.R().
		SetHeaders(headers).
		SetResult(&catalogResponse).
		Get(host + "/" + board + "/catalog.json")
	if err != nil {
		return nil, err
	}
	if response.IsError() {
		return nil, errors.New(fmt.Sprintf("Error: %s", response.String()))
	}

	return catalogResponse, nil
}
