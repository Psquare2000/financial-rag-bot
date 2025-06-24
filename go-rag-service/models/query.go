package models

type QueryRequest struct {
	Question string `json:"question"`
}

type QueryResponse struct {
	Answer string `json:"answer"`
}
