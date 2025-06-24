package handler

import (
	"net/http"

	"github.com/Psquare2000/financial-rag-bot/models"
	"github.com/Psquare2000/financial-rag-bot/service"

	"github.com/gin-gonic/gin"
)

func HandleQuery(c *gin.Context) {
	var req models.QueryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
		return
	}

	response, err := service.GetAnswerFromPythonService(req.Question)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Python service failed"})
		return
	}

	c.JSON(http.StatusOK, response)
}
