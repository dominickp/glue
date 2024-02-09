package handler

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/dominickp/glue/go/src/client"
	"github.com/gin-gonic/gin"
)

// getCLIOutputFromCatalog returns a string with the CLI output of the catalog for a particular page.
// E.g.:
//
//	Page 1
//	- Welcome to /po/! (2)
//	- No Stencil thread? What has happened to /po/ ? (1)
//	- Bookbinding (36)
//	...
func getCLIOutputFromCatalog(catalog []client.CatalogPage, page int) string {
	cli_response := "Page " + strconv.Itoa(page) + "\n"
	for _, thread := range catalog[page-1].Threads {
		subject := thread.Sub
		if subject == "" {
			subject = thread.Com
		}
		if len(subject) > 64 {
			subject = fmt.Sprintf("%.64s...", subject)
		}
		replies := strconv.Itoa(thread.Replies)
		cli_response += " - " + subject + " (" + replies + ") \n"
	}
	return cli_response
}

func HandleCatalog(c *gin.Context) {
	name := c.Param("name")
	page := c.Param("page")
	if page == "" {
		page = "1"
	}
	pageInt, err := strconv.Atoi(page)
	if err != nil {
		c.String(http.StatusBadRequest, "Invalid page number.")
	}

	catalog, err := client.GetCatalog(name)
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}

	cliResponse := getCLIOutputFromCatalog(catalog, pageInt)
	c.String(http.StatusOK, cliResponse)
}
