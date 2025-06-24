package main

import (
	"net/http"

	"github.com/Psquare2000/financial-rag-bot/handler"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":  "ok",
			"service": "financial-rag-bot",
		})
	})

	router.POST("/query", handler.HandleQuery)

	router.Run(":8088")
}
