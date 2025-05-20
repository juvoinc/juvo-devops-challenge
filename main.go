package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"regexp"
	"time"
)

type CPFRequest struct {
	CPF string `json:"cpf"`
}

type ScoreResponse struct {
	CPF   string `json:"cpf"`
	Score int    `json:"score"`
}

// Valida se o CPF contém exatamente 11 dígitos numéricos
func isValidCPF(cpf string) bool {
	match, _ := regexp.MatchString(`^\d{11}$`, cpf)
	return match
}

// Handler para gerar e retornar o score
func getScoreHandler(w http.ResponseWriter, r *http.Request) {
	var req CPFRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil || !isValidCPF(req.CPF) {
		http.Error(w, "CPF inválido. Deve conter 11 dígitos numéricos.", http.StatusBadRequest)
		return
	}

	rand.Seed(time.Now().UnixNano())
	score := rand.Intn(1001) // Score entre 0 e 1000

	resp := ScoreResponse{CPF: req.CPF, Score: score}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// Endpoint para verificação de saúde da aplicação
func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

func main() {
	http.HandleFunc("/score", getScoreHandler)
	http.HandleFunc("/health", healthHandler)

	log.Println("Servidor iniciado na porta 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
