package handler

import (
	"net/http"

	"github.com/dominickp/glue/go/src/client"
	"github.com/gin-gonic/gin"
)

func HandleCatalog(c *gin.Context) {
	name := c.Param("name")
	page := c.Param("page")
	if page == "" {
		page = "1"
	}

	catalog, err := client.GetCatalog(name)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": err.Error(),
		})
		return
	}
	c.JSON(http.StatusOK, catalog)
}
