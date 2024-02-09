package client

import (
	"encoding/json"
	"errors"
	"os"

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
		SetJSONUnmarshaler(json.Unmarshal)
}

// GetCatalog retrieves the catalog of a supported SFW board.
// The 'board' parameter specifies the board to get the catalog of (e.g., "po" for Papercraft & Origami).
func GetCatalog(board string) (interface{}, error) {

	// Check if the board is in the sfwSupportedBoardsArray
	isSupported := false
	for _, supportedBoard := range sfwSupportedBoardsArray {
		if board == supportedBoard {
			isSupported = true
			break
		}
	}
	if !isSupported {
		return "", errors.New("Board not supported.")
	}

	// Call the 4channel API to get the catalog
	catalogResponse := []CatalogPage{}
	_, err := restyClient.R().
		SetResult(&catalogResponse).
		Get(host + "/" + board + "/catalog.json")
	if err != nil {
		return "", err
	}

	return catalogResponse, nil
}
