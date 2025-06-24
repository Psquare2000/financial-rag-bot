package service

import (
	"fmt"

	"github.com/Psquare2000/financial-rag-bot/models"

	"github.com/go-resty/resty/v2"
)

func GetAnswerFromPythonService(question string) (*models.QueryResponse, error) {
	client := resty.New()

	var response models.QueryResponse
	resp, err := client.R().
		SetBody(map[string]string{"question": question}).
		SetResult(&response).
		Post("http://localhost:5000/generate-answer") // Python microservice URL

	if err != nil || resp.IsError() {
		return nil, fmt.Errorf("Failed to contact Python service")
	}

	return &response, nil
}
