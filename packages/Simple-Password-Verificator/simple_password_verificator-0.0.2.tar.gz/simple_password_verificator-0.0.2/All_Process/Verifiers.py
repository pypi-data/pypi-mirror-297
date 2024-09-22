class All_Verifiers:
    
    @staticmethod
    def eight_char(senha: str):
        if len(senha) >= 8:
            return True
        return False
    
    @staticmethod
    def number_verificator(senha: str):
        for char in senha:
            if char.isdigit() == True:
                return True
        return False
    
    @staticmethod
    def upper_verificator(senha: str):
        for char in senha:
            if char.isupper() == True:
                return True
        return False     
    
    @staticmethod
    def lower_verificator(senha: str):
        for char in senha:
            if char.islower() == True:
                return True
        return False    

    @staticmethod
    def special_char_verificator(senha: str):
        for char in senha:
            if char.isdigit() == False and char.isalpha() == False:
                return True
        return False    
    
    @staticmethod
    def space_verificator(senha: str):
        for char in senha:
            if char == " ":
                return False
        return True    
    
class Password_Verificator():    

    @staticmethod
    def __feedback(senha):
        if All_Verifiers.eight_char(senha) == True: print("\n8 Caractéres ou mais☑️") 
        else: print("\n8 Caractéres ou mais❌")

        if All_Verifiers.number_verificator(senha) == True: print("Apresenta no mínimo 1 digito☑️") 
        else: print("Apresenta no mínimo 1 digito❌")

        if All_Verifiers.upper_verificator(senha) == True: print("Apresenta no mínimo 1 letra maíuscula☑️") 
        else: print("Apresenta no mínimo 1 letra maíuscula❌")

        if All_Verifiers.lower_verificator(senha) == True: print("Apresenta no mínimo 1 letra minuscula☑️") 
        else: print("Apresenta no mínimo 1 letra minuscula❌")

        if All_Verifiers.special_char_verificator(senha) == True: print("Apresenta no mínimo 1 carácter especial☑️") 
        else: print("Apresenta no mínimo 1 carácter especial❌")

        if All_Verifiers.space_verificator(senha) == True: print("Não apresenta espaços em branco☑️") 
        else: print("Não apresenta espaços em branco❌")

    def start():
        senha = input("Olá! Informe sua senha: ")
        
        Password_Verificator.__feedback(senha)

        if All_Verifiers.eight_char(senha) == True and All_Verifiers.lower_verificator(senha) == True and All_Verifiers.number_verificator(senha) == True and All_Verifiers.upper_verificator(senha) == True and All_Verifiers.special_char_verificator(senha) == True and All_Verifiers.space_verificator(senha) == True:
            print("\nSenha válida e salva com sucesso!")

        else: 
            print("\nSenha inválida. Tente novamente.")    


