import logging
import azure.functions as func
import re

def is_valid_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos ou é um CPF inválido comum
    if len(cpf) != 11 or cpf in [cpf[0] * 11 for cpf in "0123456789"]:
        return False

    # Cálculo do primeiro dígito verificador
    sum_v1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    check_v1 = (sum_v1 * 10) % 11
    check_v1 = 0 if check_v1 == 10 else check_v1

    # Cálculo do segundo dígito verificador
    sum_v2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    check_v2 = (sum_v2 * 10) % 11
    check_v2 = 0 if check_v2 == 10 else check_v2

    # Valida os dígitos verificadores
    return check_v1 == int(cpf[9]) and check_v2 == int(cpf[10])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing CPF validation request.')

    try:
        # Obtém o CPF da requisição
        cpf = req.params.get('cpf')
        if not cpf:
            return func.HttpResponse(
                "Please provide a CPF in the query string or request body.",
                status_code=400
            )
        
        # Valida o CPF
        if is_valid_cpf(cpf):
            return func.HttpResponse(f"The CPF {cpf} is valid.", status_code=200)
        else:
            return func.HttpResponse(f"The CPF {cpf} is invalid.", status_code=400)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(
            "An error occurred while processing your request.",
            status_code=500
        )
