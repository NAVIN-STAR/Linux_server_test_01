from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import schemas, models
from ..database import get_db
from ..auth_dependencies import get_current_user

router=APIRouter()

@router.get('/')
def Welcome():
    return {'message':"welcome"}

#Insertion routes
@router.post('/coffees/',response_model=List[schemas.ReadCoffee])
def Create_Coffee(coffees:List[schemas.CoffeeCreate],db:Session=Depends(get_db)):
    db_coffees=[]
    try:
        for coffee in coffees:

            coffee_name=coffee.name.strip().lower() #Preprocessing if name contains extra space
            existing_name=db.query(models.Coffee).filter(models.Coffee.name==coffee_name).first()
            if existing_name:
                raise HTTPException(status_code=400,detail=f'{coffee_name} already exists')

            db_coffee=models.Coffee(**coffee.model_dump())
            db_coffee.name=db_coffee.name.lower()
            db.add(db_coffee)
            db_coffees.append(db_coffee)

        db.commit()
        for db_coffee in db_coffees:
            db.refresh(db_coffee)

        return [schemas.ReadCoffee.model_validate(db_coffee) for db_coffee in db_coffees]
    except IntegrityError:
        db.rollback()  #
        raise HTTPException(status_code=400, detail="A coffee with the same name already exists.")


#Display Routes
@router.get('/allcoffees/',response_model=List[schemas.ReadCoffee])
def Get_Coffees(skip:int=0,limit:int=100,db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    coffees=db.query(models.Coffee).offset(skip).limit(limit).all()
    return coffees

@router.get('/coffees/{coffee_name}',response_model=schemas.ReadCoffee)
def Get_Coffee(coffee_name:str,db:Session=Depends(get_db)):
    coffee_name=coffee_name.strip().lower()
    db_coffee= db.query(models.Coffee).filter( models.Coffee.name== coffee_name).first()
    if not db_coffee:
        raise HTTPException(status_code=404,detail='Coffee not found')
    return (schemas.ReadCoffee.model_validate(db_coffee))




#Deletion Routes
@router.delete('/coffees/delete/')
def Delete_Coffee(coffee_names:str,db:Session=Depends(get_db)):
    names_to_delete=coffee_names.lower().split(',')
    db_coffees=db.query(models.Coffee).filter(models.Coffee.name.in_(names_to_delete)).all()
    found_ids=[coffee.id for coffee in db_coffees]
    found_names=[coffee.name for coffee in db_coffees]
    missing_names=[id for id in names_to_delete if id not in found_names]

    db.query(models.Coffee).filter(models.Coffee.name.in_(found_names)).delete(synchronize_session=False)
    db.commit()

    if missing_names:
        raise HTTPException(status_code=404, detail={"message":"Some coffees are not found","missing_names":missing_names})

    return {"message": "Coffees deleted successfully", "deleted_ids": list(found_ids),"deleted_coffee_names":list(found_names)}


    
#Updation Routes
@router.patch('/coffees/PriceUpdate/',response_model=List[schemas.ReadCoffee])
def Update_coffee(price_update_details:List[schemas.UpdateCoffee],db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    coffee_names=[coffee_name.name.strip().lower() for coffee_name in price_update_details]

    db_coffees=db.query(models.Coffee).filter(models.Coffee.name.in_(coffee_names)).all()

    coffee_dict={coffee.name: coffee for coffee in db_coffees}

    missing_names=[coffee_name for coffee_name in coffee_names if coffee_name not in coffee_dict]

    if missing_names:
        raise HTTPException(status_code=404,detail={"message":"Some coffes are missing","missing_coffee_names":missing_names})
    
    for price_upate_detail in price_update_details:
        coffee_dict[price_upate_detail.name.strip().lower()].price=price_upate_detail.price
    
    db.commit()
    for db_coffee in db_coffees:
        db.refresh(db_coffee)

    
    return ([schemas.ReadCoffee.model_validate(db_coffee) for db_coffee in db_coffees])
    


    
    # for price_update_detail in price_update_details:
    #     coffee_name=price_update_detail.name.strip().lower()
    #     db_coffee=db.query(models.Coffee).filter(models.Coffee.name==coffee_name).first()
        
    #     if not db_coffee:
    #         raise HTTPException(status_code=404,detail={"message":f"{coffee_name} is not found"})

    #     db_coffee.price=price_update_detail.price
    #     updated_db_coffees.append(db_coffee)

    # db.commit()
    # for updated_db_coffee in updated_db_coffees:
    #     db.refresh(updated_db_coffee)
    
    # return [schemas.ReadCoffee.model_validate(updated_db_coffee.__dict__) for updated_db_coffee in updated_db_coffees]






