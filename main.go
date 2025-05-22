package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "os"
    "time"
)

type ScoreRequest struct {
    CPF string `json:"cpf"`
}

type ScoreResponse struct {
    CPF   string `json:"cpf"`
    Score int    `json:"score"`
}

func scoreHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Método não permitido", http.StatusMethodNotAllowed)
        return
    }

    var req ScoreRequest
    decoder := json.NewDecoder(r.Body)
    if err := decoder.Decode(&req); err != nil {
        http.Error(w, `{"error":"bad request"}`, http.StatusBadRequest)
        return
    }

    rand.Seed(time.Now().UnixNano())

    // Gera score aleatório entre 300 e 850
    score := rand.Intn(551) + 300

    response := ScoreResponse{CPF: req.CPF, Score: score}

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    log.Println("Iniciando servidor na porta", port)

    http.HandleFunc("/score", scoreHandler)
    http.HandleFunc("/health", healthHandler)

    server := &http.Server{
        Addr:         ":" + port,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    log.Fatal(server.ListenAndServe())
}
