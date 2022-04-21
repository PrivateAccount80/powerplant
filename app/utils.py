from typing import List
from . import schemas
import copy


def sort_powerplants_by_merit_order(payload: schemas.Payload):
    payload.powerplants.sort(key=lambda p:price_to_generate_MWH(fuels=payload.fuels, powerplant=p))

def price_to_generate_MWH(fuels: schemas.Fuels, powerplant: schemas.Powerplant):
    if powerplant.type == "windturbine":
        return 0
    
    fuels_price = fuels[powerplant.type]
    return fuels_price / powerplant.efficiency

def handle_wind_in_pmax(payload: schemas.Payload):
    for pwp in payload.powerplants:
        if pwp.type == "windturbine":
            pwp.pmax = round(pwp.pmax / 100 * payload.fuels.windturbine, 1)



def load_energy_by_backtraking(total_load: int, powerplants: List[schemas.Powerplant], res = []):
    pwp = powerplants[0]
    for i in range(10,-1,-2): # 100%, 80%, 60%, 40%, 20%, 0%
        new_res = copy.deepcopy(res)
        loaded_energy = 0
        
        new_pmax = round(pwp.pmax*(i/10), 1)
        
        if (total_load < pwp.pmin or total_load < 1 or new_pmax < 1):
            new_res.append(schemas.PowerplantResult(name=pwp.name, p=0))
        elif (total_load <= pwp.pmax):
            new_res.append(schemas.PowerplantResult(name=pwp.name, p=total_load))
            loaded_energy = total_load
        else:
            loaded_energy = new_pmax
            new_res.append(schemas.PowerplantResult(name=pwp.name, p=new_pmax))
        
        if (len(powerplants) > 1):
            res_energy, new_res = load_energy_by_backtraking(total_load - loaded_energy, powerplants[1:], new_res)
            loaded_energy += res_energy
        
        
        #Cancel the loop if
        if (loaded_energy == total_load):
            break
        if (loaded_energy < pwp.pmin or loaded_energy < 1 or new_pmax < 1):
            break
    
    return loaded_energy, new_res
