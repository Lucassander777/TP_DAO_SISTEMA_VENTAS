from repositories.bulto_dao import BultoDAO
from repositories.venta_dao import VentaDAO
from repositories.inventario_dao import InventarioDao
from repositories.lote_dao import LoteDAO
from repositories.compras_dao import ComprasDAO
from repositories.clientes_dao import ClienteDAO
from repositories.auditoria_dao import AuditoriaDAO
from repositories.reportes_dao import ReportesDAO

from services.logistica_service import LogisticaService
from services.ventas_service import VentaService
from services.inventario_service import InventarioService
from services.lote_service import LoteService
from services.compras_service import ComprasService
from services.clientes_service import ClienteService
from services.auditoria_service import AuditoriaService
from services.reportes_service import ReportesService

from ui.menu_principal import iniciar_interfaz

def main():

    # 1. Instanciar los DAOs
    bulto_dao = BultoDAO()
    venta_dao = VentaDAO()
    inventario_dao = InventarioDao()
    lote_dao = LoteDAO()
    compras_dao = ComprasDAO()
    cliente_dao = ClienteDAO()
    auditoria_dao = AuditoriaDAO()
    reporte_dao = ReportesDAO()
    

    # 2. Instanciar los Servicios
    inventario_service = InventarioService(inventario_dao)
    logistica_service = LogisticaService(bulto_dao)
    ventas_service = VentaService(venta_dao, inventario_service)
    lote_service = LoteService(lote_dao, inventario_service)
    
    # Aquí pasamos compras_dao e inventario_service:
    compras_service = ComprasService(compras_dao, inventario_service)
    
    cliente_service = ClienteService(cliente_dao)
    auditoria_service = AuditoriaService(auditoria_dao)
    reporte_service = ReportesService(reporte_dao)

    # 3. Arrancar la interfaz gráfica
    iniciar_interfaz(logistica_service, ventas_service, lote_service, compras_service, cliente_service, auditoria_service, reporte_service)

if __name__ == "__main__":
    main()
