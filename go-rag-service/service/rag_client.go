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
		Post("http://localhost:8000/query") // Python microservice URL

	if err != nil || resp.IsError() {
		println("this is the error :", err)
		return nil, fmt.Errorf("failed to contact python service")
	}

	return &response, nil
}
