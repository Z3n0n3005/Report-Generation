class Segment:
    def __init__(self, header:str="", content:str=""):
        self.header = header
        self.content = content

    def __str__(self) -> str:
        result = "-----------\n"
        result += "HEADER: " 
        result += self.header + "\n"
        result += "CONTENT: \n"
        result += self.content + "\n"
        return result

    def set_header(self, header:str):
        self.header = header
    
    def set_content(self, content:str):
        self.content = content

    def get_header(self):
        return self.header

    def get_content(self):
        return self.content

    def add_content(self, content:str):
        if(content == None):
            return 
        
        self.content += self.clean_content(content) 

    def clean_content(self, content:str) -> str:
        content = content.strip()
        content = content.lower()
        # Remove new line
        content = ' '.join(content.splitlines())
        # if(not content.endswith(".")):
        #     content += ". "
        # else: 
        #     content += " "
        return content                
def clean_content(content:str) -> str:
    content = content.strip()
    content = content.lower()
    # Remove new line
    content = ' '.join(content.splitlines())
    # if(not content.endswith(".")):
    #     content += ". "
    # else: 
    #     content += " "
    return content 

if __name__ == "__main__":
    print(clean_content("Efficiency and fairness in determining who gets what and when are the two major objectives of economists thinking about scarcity, and many interesting matchmaking and market design solutions have been proposed Such mechanisms have been proposed previously in non-human contexts to manage scarcity in, for example, traffic Karma and the aforementioned choice system are different from other token-based mechanisms that have been implemented and proposed in the past, including those that use tradable credits Figure The example illustrates that karma is similar in spirit to the 'universal currency' of reputation Further, the example also illustrates another feature of karma, as was mentioned above, that distinguishes karma from fixed-value tokens and from other forms of rules ensuring turn-taking: it allows individuals to dynamically express how intense their private preference for the resource is. Clearly, such a mechanism may be advantageous when preference intensities/urgencies in the population are heterogeneous and not perfectly correlated over time. Indeed, To date, the literature on karma focused on the theoretical properties of the mechanism compared with random allocation and other domain-specific schemes such as dynamic pricing or max-min allocation Our main findings summarize as follows. Overall, compared with random allocation, karma leads to substantial efficiency gains, and these gains benefit almost all participants. In fact, only non-adopters, that is, individuals who do not participate in karma bidding actively themselves, do not benefit and may be worse off. The treatment variations suggest that benefits are particularly pronounced in situations when preference intensities are dynamically more intense and less frequent, and the bidding scheme is designed to be minimal (i.e., binary). These findings provide a first benchmark that karma may be used beneficially in human interactions. Our study also points in several directions for further theoretical and experimental investigation."))
