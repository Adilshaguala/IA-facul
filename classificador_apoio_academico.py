"""Entrada de linha de comandos: prepara os dados, treina e avalia os modelos."""

from treino import treinar_e_guardar


if __name__ == "__main__":
    pacote = treinar_e_guardar()
    print("Divisão estratificada: 75% treino / 25% teste; semente 42.")
    print(pacote["resultados"].to_string(index=False))
    print("\nDados de teste: dados_teste.csv")
    print("Modelos: artefactos/modelos.joblib")
    print("Interface: python -m streamlit run app.py")
