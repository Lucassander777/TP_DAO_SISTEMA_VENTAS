from abc import ABC, abstractmethod

class EstadoBulto(ABC):
    @abstractmethod
    def precintar(self, bulto):
        pass

    @abstractmethod
    def despachar(self, bulto):
        pass

    @abstractmethod
    def recibir(self, bulto):
        pass

    @abstractmethod
    def verificar(self, bulto):
        pass

    @abstractmethod
    def rechazar(self, bulto):
        pass

class Preparado(EstadoBulto):
    def precintar(self, bulto):
        # Lógica para precintar el bulto y cambiar el estado
        pass

    def despachar(self, bulto):
        pass

    def recibir(self, bulto):
        pass

    def verificar(self, bulto):
        pass

    def rechazar(self, bulto):
        pass

class Precintado(EstadoBulto):
    def precintar(self, bulto):
        # Lógica para precintar el bulto y cambiar el estado
        pass
    
    def despachar(self, bulto):
        pass
    
    def recibir(self, bulto):
        pass
    
    def verificar(self, bulto):
        pass
    
    def rechazar(self, bulto):
        pass

class EnTransito(EstadoBulto):
    def precintar(self, bulto):
        pass
    
    def despachar(self, bulto):
        # Lógica para despachar el bulto y cambiar el estado
        pass
    
    def recibir(self, bulto):
        pass
    
    def verificar(self, bulto):
        pass
    
    def rechazar(self, bulto):
        pass

class Recibido(EstadoBulto):
    def precintar(self, bulto):
        pass
    
    def despachar(self, bulto):
        pass
    
    def recibir(self, bulto):
        # Lógica para recibir el bulto y cambiar el estado
        pass
    
    def verificar(self, bulto):
        pass
    
    def rechazar(self, bulto):
        pass

class Verificado(EstadoBulto):
    def precintar(self, bulto):
        pass
    
    def despachar(self, bulto):
        pass
    
    def recibir(self, bulto):
        pass
    
    def verificar(self, bulto):
        # Lógica para verificar el bulto y cambiar el estado
        pass
    
    def rechazar(self, bulto):
        pass

class Rechazado(EstadoBulto):
    def precintar(self, bulto):
        pass
    
    def despachar(self, bulto):
        pass
    
    def recibir(self, bulto):
        pass
    
    def verificar(self, bulto):
        pass
    
    def rechazar(self, bulto):
        # Lógica para rechazar el bulto y cambiar el estado
        pass

    

    