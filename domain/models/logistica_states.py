from abc import ABC, abstractmethod
from domain.exceptions import TransicionEstadoInvalidaException

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
        bulto.estado_actual = Precintado()

    def despachar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe estar precintado para despacharse.")

    def recibir(self, bulto):
        raise TransicionEstadoInvalidaException("No se puede recibir un bulto recién preparado.")

    def verificar(self, bulto):
        raise TransicionEstadoInvalidaException("No se puede verificar un bulto recién preparado.")

    def rechazar(self, bulto):
        raise TransicionEstadoInvalidaException("No se puede rechazar un bulto recién preparado.")

class Precintado(EstadoBulto):
    def precintar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está precintado.")
    
    def despachar(self, bulto):
        bulto.estado_actual = EnTransito()
    
    def recibir(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe despacharse antes de recibirse.")
    
    def verificar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe recibirse antes de verificarse.")
    
    def rechazar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe recibirse antes de rechazarse.")

class EnTransito(EstadoBulto):
    def precintar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está en tránsito.")
    
    def despachar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya fue despachado.")
    
    def recibir(self, bulto):
        bulto.estado_actual = Recibido()
    
    def verificar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe recibirse antes de verificarse.")
    
    def rechazar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto debe recibirse antes de rechazarse.")

class Recibido(EstadoBulto):
    def precintar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya fue recibido.")
    
    def despachar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya fue recibido.")
    
    def recibir(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya fue recibido.")
    
    def verificar(self, bulto):
        bulto.estado_actual = Verificado()
    
    def rechazar(self, bulto):
        bulto.estado_actual = Rechazado()

class Verificado(EstadoBulto):
    def precintar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está verificado, ciclo terminado.")
    
    def despachar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está verificado, ciclo terminado.")
    
    def recibir(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está verificado, ciclo terminado.")
    
    def verificar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está verificado.")
    
    def rechazar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está verificado y no puede rechazarse.")

class Rechazado(EstadoBulto):
    def precintar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto fue rechazado, ciclo terminado.")
    
    def despachar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto fue rechazado, ciclo terminado.")
    
    def recibir(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto fue rechazado, ciclo terminado.")
    
    def verificar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto fue rechazado y no puede verificarse.")
    
    def rechazar(self, bulto):
        raise TransicionEstadoInvalidaException("El bulto ya está rechazado.")

    

    