import asyncio
import aiohttp
import random

URL_API = "https://api.juvo.turatti.xyz/score"  # Altere para sua URL
TOTAL_REQUESTS = 1000
CONCURRENT_REQUESTS = 100  # Limite de concorrência

# Gera CPF válido
def generate_cpf():
    def mod11(s, m):
        soma = sum(int(s[i]) * (m - i) for i in range(len(s)))
        resto = 11 - (soma % 11)
        return '0' if resto >= 10 else str(resto)

    base = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    d1 = mod11(base, 10)
    d2 = mod11(base + d1, 11)
    return base + d1 + d2

# Função para uma única requisição
async def send_request(session, sem):
    cpf = generate_cpf()
    payload = {"cpf": cpf}
    headers = {"Content-Type": "application/json"}

    async with sem:  # Limita o número de requisições simultâneas
        try:
            async with session.post(URL_API, json=payload, timeout=5) as response:
                status = response.status
                data = await response.text()
                print(f"{status}: {data}")
        except asyncio.TimeoutError:
            print("Timeout")
        except Exception as e:
            print(f"Erro: {e}")

# Função principal para coordenar o stress test
async def main():
    sem = asyncio.Semaphore(CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(send_request(session, sem)) for _ in range(TOTAL_REQUESTS)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

