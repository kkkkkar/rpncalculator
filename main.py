from src.calculator import calculate


def main():
    print("Калькулятор с обратной польской нотацией")
    print("Поддерживаемые операции: +, -, *, /, ^, скобки")
    print("Введите 'exit' для выхода")

    while True:
        try:
            expression = input("\nВведите выражение: ").strip()

            if expression.lower() in ['exit', 'quit', 'выход']:
                print("До свидания!")
                break

            if not expression:
                continue

            result = calculate(expression)
            print(f"Результат: {result}")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена")
            break
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()
