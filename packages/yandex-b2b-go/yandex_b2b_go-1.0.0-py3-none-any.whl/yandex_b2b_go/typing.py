import enum
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union

from yandex_b2b_go.errors import ValidationError
from yandex_b2b_go.utils import error_string


class Service(enum.Enum):
    taxi: str = 'taxi'
    drive: str = 'drive'
    eats: str = 'eats2'
    tanker: str = 'tanker'
    cargo: str = 'cargo'
    travel: str = 'travel'
    grocery: str = 'grocery'


class Role(enum.Enum):
    department_manager: str = 'department_manager'
    department_secretary: str = 'department_secretary'
    agent_admin: str = 'agent_admin'
    agent_delegate: str = 'agent_delegate'
    client_manager: str = 'client_manager'


class Geo(enum.Enum):
    circle: str = 'circle'


class SupportedRequirementType(enum.Enum):
    select: str = 'select'
    boolean: str = 'boolean'


class PromocodeOrderStatus(enum.Enum):
    creation_success: str = 'creation_success'
    creation_failed: str = 'creation_failed'
    cancellation_success: str = 'cancellation_success'
    cancellation_failed: str = 'cancellation_failed'
    pending: str = 'pending'


class PromocodeOrderService(enum.Enum):
    taxi: str = 'taxi'
    grocery: str = 'grocery'
    eats: str = 'eats'


class PromocodeOrderCancelStatus(enum.Enum):
    cancelled: str = 'cancelled'


class SortingOrder(enum.Enum):
    asc: str = 'asc'
    desc: str = 'desc'


class TimeRestrictionType(enum.Enum):
    weekly_date: str = 'weekly_date'
    range_date: str = 'range_date'


class Day(enum.Enum):
    monday: str = 'mo'
    tuesday: str = 'tu'
    wednesday: str = 'we'
    thursday: str = 'th'
    friday: str = 'fr'
    saturday: str = 'sa'
    sunday: str = 'su'


class MeasureKind(enum.Enum):
    money: str = 'money'
    volume: str = 'volume'


class MeasurePeriod(enum.Enum):
    day: str = 'day'
    week: str = 'week'
    month: str = 'month'


class CostCenterFormat(enum.Enum):
    select: str = 'select'
    text: str = 'text'
    mixed: str = 'mixed'


class TaxiOrderDetailsTariffItemType(enum.Enum):
    price: str = 'price'
    icon: str = 'icon'
    comment: str = 'comment'
    switch_label: str = 'switch_label'
    switch_clarification: str = 'switch_clarification'
    requirement: str = 'requirement'


class ApproveRole(enum.Enum):
    client: str = 'client'
    manager: str = 'department_manager'


class GeoHotelPolicyType(enum.Enum):
    included: str = 'included'
    excluded: str = 'excluded'


class CountriesRestriction(enum.Enum):
    rus: str = 'rus'
    cis: str = 'cis'


class TravelClass(enum.Enum):
    economy: str = 'economy'
    business: str = 'business'
    premium: str = 'premium'
    first: str = 'first'


class SortingField(enum.Enum):
    due_date: str = 'due_date'
    finished_date: str = 'finished_date'


class SortingDirection(enum.Enum):
    asc: int = 1
    desc: int = -1


class TaxiOrderCancelRulesState(enum.Enum):
    free: str = 'free'
    paid: str = 'paid'
    minimal: str = 'minimal'


class TaxiOrderCancelStatus(enum.Enum):
    cancelled: str = 'cancelled'


class EatsOrdersListRequest:
    user_ids: List[str]

    def __init__(self, user_ids: List[str]):
        if len(user_ids) > 100:
            user_ids = user_ids[:100]
        self.user_ids = user_ids

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'user_ids': self.user_ids}
        return data


class EatDiscount:
    sum: str
    vat: str
    with_vat: str
    sales_tax: Optional[str] = None
    total: Optional[str] = None

    def __init__(
        self,
        sum: str,
        vat: str,
        with_vat: str,
        sales_tax: Optional[str] = None,
        total: Optional[str] = None,
    ):
        self.sum = sum
        self.vat = vat
        self.with_vat = with_vat
        self.sales_tax = sales_tax
        self.total = total

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'sum': self.sum,
            'vat': self.vat,
            'with_vat': self.with_vat,
        }
        if self.sales_tax is not None:
            data['sales_tax'] = self.sales_tax
        if self.total is not None:
            data['total'] = self.total

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            sum=json['sum'],
            vat=json['vat'],
            with_vat=json['with_vat'],
            sales_tax=json.get('sales_tax'),
            total=json.get('total'),
        )


class TransactionsTotal:
    sum: Optional[str] = None
    with_vat: Optional[str] = None

    def __init__(
        self,
        sum: Optional[str] = None,
        with_vat: Optional[str] = None,
    ):
        self.sum = sum
        self.with_vat = with_vat

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.sum is not None:
            data['sum'] = self.sum
        if self.with_vat is not None:
            data['with_vat'] = self.with_vat

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(sum=json.get('sum'), with_vat=json.get('with_vat'))


class EatOrderModifier:
    name: str
    cost: str
    vat: str
    cost_with_vat: str
    count: Optional[int] = None

    def __init__(
        self,
        name: str,
        cost: str,
        vat: str,
        cost_with_vat: str,
        count: Optional[int] = None,
    ):
        self.name = name
        self.cost = cost
        self.vat = vat
        self.cost_with_vat = cost_with_vat
        self.count = count

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'cost': self.cost,
            'vat': self.vat,
            'cost_with_vat': self.cost_with_vat,
        }
        if self.count is not None:
            data['count'] = self.count

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            name=json['name'],
            cost=json['cost'],
            vat=json['vat'],
            cost_with_vat=json['cost_with_vat'],
            count=json.get('count'),
        )


class EatOrderCalculation:
    name: str
    cost: str
    vat: str
    cost_with_vat: str
    modifiers: Optional[List[EatOrderModifier]] = None
    count: Optional[int] = None

    def __init__(
        self,
        name: str,
        cost: str,
        vat: str,
        cost_with_vat: str,
        modifiers: Optional[List[EatOrderModifier]] = None,
        count: Optional[int] = None,
    ):
        self.name = name
        self.cost = cost
        self.vat = vat
        self.cost_with_vat = cost_with_vat
        self.modifiers = modifiers
        self.count = count

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'cost': self.cost,
            'vat': self.vat,
            'cost_with_vat': self.cost_with_vat,
        }
        if self.modifiers is not None:
            data['modifiers'] = [modifier.serialize() for modifier in self.modifiers]
        if self.count is not None:
            data['count'] = self.count

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        modifiers = None
        if 'modifiers' in json:
            modifiers = [EatOrderModifier.new(modifier) for modifier in json['modifiers']]

        return cls(
            name=json['name'],
            cost=json['cost'],
            vat=json['vat'],
            cost_with_vat=json['cost_with_vat'],
            modifiers=modifiers,
            count=json.get('count'),
        )


class CostCenter:
    id: str
    title: str
    value: str

    def __init__(self, id: str, title: str, value: str):
        self.id = id
        self.title = title
        self.value = value

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'title': self.title,
            'value': self.value,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['id'], title=json['title'], value=json['value'])


class EatOrderItemResponse:
    id: str
    user_id: str
    status: str
    created_at: str
    department_id: Optional[str] = None
    closed_at: Optional[str] = None
    restaurant_name: Optional[str] = None
    destination_address: Optional[str] = None
    order_calculation: Optional[List[EatOrderCalculation]] = None
    final_cost: Optional[str] = None
    vat: Optional[str] = None
    final_cost_with_vat: Optional[str] = None
    corp_discount: Optional[EatDiscount] = None
    corp_discount_reverted: Optional[bool] = None
    currency: Optional[str] = None
    eats_cost_centers: Optional[List[CostCenter]] = None
    transactions_total: Optional[TransactionsTotal] = None

    def __init__(
        self,
        id: str,
        user_id: str,
        status: str,
        created_at: str,
        department_id: Optional[str] = None,
        closed_at: Optional[str] = None,
        restaurant_name: Optional[str] = None,
        destination_address: Optional[str] = None,
        order_calculation: Optional[List[EatOrderCalculation]] = None,
        final_cost: Optional[str] = None,
        vat: Optional[str] = None,
        final_cost_with_vat: Optional[str] = None,
        corp_discount: Optional[EatDiscount] = None,
        corp_discount_reverted: Optional[bool] = None,
        currency: Optional[str] = None,
        eats_cost_centers: Optional[List[CostCenter]] = None,
        transactions_total: Optional[TransactionsTotal] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.created_at = created_at
        self.department_id = department_id
        self.closed_at = closed_at
        self.restaurant_name = restaurant_name
        self.destination_address = destination_address
        self.order_calculation = order_calculation
        self.final_cost = final_cost
        self.vat = vat
        self.final_cost_with_vat = final_cost_with_vat
        self.corp_discount = corp_discount
        self.corp_discount_reverted = corp_discount_reverted
        self.currency = currency
        self.eats_cost_centers = eats_cost_centers
        self.transactions_total = transactions_total

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at,
        }
        if self.department_id is not None:
            data['department_id'] = self.department_id
        if self.closed_at is not None:
            data['closed_at'] = self.closed_at
        if self.restaurant_name is not None:
            data['restaurant_name'] = self.restaurant_name
        if self.destination_address is not None:
            data['destination_address'] = self.destination_address
        if self.order_calculation is not None:
            data['order_calculation'] = [order_calculate.serialize() for order_calculate in self.order_calculation]
        if self.final_cost is not None:
            data['final_cost'] = self.final_cost
        if self.vat is not None:
            data['vat'] = self.vat
        if self.final_cost_with_vat is not None:
            data['final_cost_with_vat'] = self.final_cost_with_vat
        if self.corp_discount is not None:
            data['corp_discount'] = self.corp_discount.serialize()
        if self.corp_discount_reverted is not None:
            data['corp_discount_reverted'] = self.corp_discount_reverted
        if self.currency is not None:
            data['currency'] = self.currency
        if self.eats_cost_centers is not None:
            data['eats_cost_centers'] = [cost_center.serialize() for cost_center in self.eats_cost_centers]
        if self.transactions_total is not None:
            data['transactions_total'] = self.transactions_total.serialize()

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        order_calculation = None
        corp_discount = None
        eats_cost_centers = None
        transactions_total = None
        if 'order_calculation' in json:
            order_calculation = [
                EatOrderCalculation.new(order_calculate) for order_calculate in json['order_calculation']
            ]
        if 'corp_discount' in json:
            corp_discount = EatDiscount.new(json['corp_discount'])
        if 'eats_cost_centers' in json:
            eats_cost_centers = [CostCenter.new(cost_center) for cost_center in json['eats_cost_centers']]
        if 'transactions_total' in json:
            transactions_total = TransactionsTotal.new(json['transactions_total'])

        return cls(
            id=json['id'],
            user_id=json['user_id'],
            status=json['status'],
            created_at=json['created_at'],
            department_id=json.get('department_id'),
            closed_at=json.get('closed_at'),
            restaurant_name=json.get('restaurant_name'),
            destination_address=json.get('destination_address'),
            order_calculation=order_calculation,
            final_cost=json.get('final_cost'),
            vat=json.get('vat'),
            final_cost_with_vat=json.get('final_cost_with_vat'),
            corp_discount=corp_discount,
            corp_discount_reverted=json.get('corp_discount_reverted'),
            currency=json.get('currency'),
            eats_cost_centers=eats_cost_centers,
            transactions_total=transactions_total,
        )


class EatOrderListResponse:
    orders: List[EatOrderItemResponse]
    limit: Optional[int] = None
    cursor: Optional[str] = None
    sorting_order: Optional[SortingOrder] = None

    def __init__(
        self,
        orders: List[EatOrderItemResponse],
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        sorting_order: Optional[SortingOrder] = None,
    ):
        self.orders = orders
        self.limit = limit
        self.cursor = cursor
        self.sorting_order = sorting_order

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'orders': [order.serialize() for order in self.orders]}
        if self.limit is not None:
            data['limit'] = self.limit
        if self.cursor is not None:
            data['cursor'] = self.cursor
        if self.sorting_order is not None:
            data['sorting_order'] = self.sorting_order.value

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        sorting_order = None
        if 'sorting_order' in json:
            sorting_order = SortingOrder(json['sorting_order'])
        return cls(
            orders=[EatOrderItemResponse.new(order) for order in json['orders']],
            limit=json.get('limit'),
            cursor=json.get('cursor'),
            sorting_order=sorting_order,
        )


class SupportedRequirementSelectOptionResponse:
    name: str
    label: str
    title: str
    weight: Optional[float] = None
    max_count: Optional[int] = None
    value: Optional[float] = None

    def __init__(
        self,
        name: str,
        label: str,
        title: str,
        weight: Optional[float] = None,
        max_count: Optional[int] = None,
        value: Optional[float] = None,
    ):
        self.name = name
        self.label = label
        self.title = title
        self.weight = weight
        self.max_count = max_count
        self.value = value

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'label': self.label,
            'title': self.title,
        }

        if self.weight is not None:
            data['weight'] = self.weight
        if self.max_count is not None:
            data['max_count'] = self.max_count
        if self.value is not None:
            data['value'] = self.value

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            name=json['name'],
            label=json['label'],
            title=json['title'],
            weight=json.get('weight'),
            max_count=json.get('max_count'),
            value=json.get('value'),
        )


class SupportedRequirementSelectResponse:
    type: str
    option: List[SupportedRequirementSelectOptionResponse]

    def __init__(
        self,
        type: str,
        option: List[SupportedRequirementSelectOptionResponse],
    ):
        self.type = type
        self.option = option

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'type': self.type,
            'option': [option.serialize() for option in self.option],
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            type=json['type'],
            option=[SupportedRequirementSelectOptionResponse.new(option) for option in json['options']],
        )


class SupportedRequirementItemResponse:
    name: str
    label: str
    glued: Optional[bool] = None
    type: Optional[SupportedRequirementType] = None
    multiselect: Optional[bool] = None
    max_weight: Optional[float] = None
    select: Optional[SupportedRequirementSelectResponse] = None

    def __init__(
        self,
        name: str,
        label: str,
        glued: Optional[bool] = None,
        type: Optional[SupportedRequirementType] = None,
        multiselect: Optional[bool] = None,
        max_weight: Optional[float] = None,
        select: Optional[SupportedRequirementSelectResponse] = None,
    ):
        self.name = name
        self.label = label
        self.glued = glued
        self.type = type
        self.multiselect = multiselect
        self.max_weight = max_weight
        self.select = select

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'name': self.name, 'label': self.label}

        if self.glued is not None:
            data['glued'] = self.glued
        if self.type is not None:
            data['type'] = self.type.value
        if self.multiselect is not None:
            data['multiselect'] = self.multiselect
        if self.max_weight is not None:
            data['max_weight'] = self.max_weight
        if self.select is not None:
            data['select'] = self.select.serialize()

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        type = None
        select = None

        if 'type' in json:
            type = SupportedRequirementType(json['type'])
        if 'select' in json:
            select = SupportedRequirementSelectResponse.new(json['select'])

        return cls(
            name=json['name'],
            label=json['label'],
            glued=json.get('glued'),
            type=type,
            multiselect=json.get('multiselect'),
            max_weight=json.get('max_weight'),
            select=select,
        )


class TariffClassItemResponse:
    name: str
    name_translate: str
    supported_requirements: List[SupportedRequirementItemResponse]

    def __init__(
        self,
        name: str,
        name_translate: str,
        supported_requirements: List[SupportedRequirementItemResponse],
    ):
        self.name = name
        self.name_translate = name_translate
        self.supported_requirements = supported_requirements

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'name_translate': self.name_translate,
            'supported_requirements': [
                supported_requirement.serialize() for supported_requirement in self.supported_requirements
            ],
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            name=json['name'],
            name_translate=json['name_translate'],
            supported_requirements=[
                SupportedRequirementItemResponse.new(supported_requirement)
                for supported_requirement in json['supported_requirements']
            ],
        )


class ZoneInfoResponse:
    tariff_classes: List[TariffClassItemResponse]

    def __init__(self, tariff_classes: List[TariffClassItemResponse]):
        self.tariff_classes = tariff_classes

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'tariff_classes': [tariff_class.serialize() for tariff_class in self.tariff_classes],
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            tariff_classes=[TariffClassItemResponse.new(tariff_class) for tariff_class in json['tariff_classes']],
        )


class GeoCircle:
    center: List[float]
    radius: Union[int, float]

    def __init__(self, lat: float, lon: float, radius: int):
        if not isinstance(lat, (float, int, Decimal)):
            raise ValidationError(error_string('lat', lat, '(float, int, Decimal)'))
        if not isinstance(lon, (float, int, Decimal)):
            raise ValidationError(error_string('lon', lon, '(float, int, Decimal)'))
        if not isinstance(radius, (int, float)):
            raise ValidationError(error_string('radius', radius, '(int, float)'))
        self.center = [lat, lon]
        self.radius = radius

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'center': self.center, 'radius': self.radius}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            lat=json['center'][0],
            lon=json['center'][1],
            radius=json['radius'],
        )


class GeoRestrictions:
    name: str
    geo_type: Geo
    geo: Union[GeoCircle]

    def __init__(self, name: str, geo_type: Geo, geo: Union[GeoCircle]):
        if not isinstance(name, str):
            raise ValidationError(error_string('name', name, 'str'))
        self.name = name
        if not isinstance(geo_type, Geo):
            raise ValidationError(error_string('geo_type', geo_type, 'Geo'))
        self.geo_type = geo_type
        if not isinstance(geo, (GeoCircle,)):
            raise ValidationError(error_string('geo', geo, '(GeoCircle)'))
        self.geo = geo

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'geo_type': self.geo_type.value,
            'geo': self.geo.serialize(),
        }

        return data


class GeoRestrictionsItemResponse(GeoRestrictions):
    id: str

    def __init__(
        self,
        id: str,
        name: str,
        geo_type: Geo,
        geo: Union[GeoCircle],
    ):
        super().__init__(name=name, geo_type=geo_type, geo=geo)
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize(), 'id': self.id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        geo = GeoCircle.new(json['geo'])

        return cls(
            id=json['id'],
            name=json['name'],
            geo_type=Geo(json['geo_type']),
            geo=geo,
        )


class GeoRestrictionsListResponse:
    items: List[GeoRestrictionsItemResponse]
    limit: int
    amount: int
    offset: int

    def __init__(
        self,
        items: List[GeoRestrictionsItemResponse],
        limit: int,
        amount: int,
        offset: int,
    ):
        self.items = items
        self.limit = limit
        self.amount = amount
        self.offset = offset

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [geo_restrictions.serialize() for geo_restrictions in self.items],
            'limit': self.limit,
            'amount': self.amount,
            'offset': self.offset,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[GeoRestrictionsItemResponse.new(geo_restrictions) for geo_restrictions in json['items']],
            limit=json['limit'],
            amount=json['amount'],
            offset=json['offset'],
        )


class GeoRestrictionsResponse:
    id: str

    def __init__(self, id: str):
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'id': self.id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['id'])


class CodeUsage:
    used_at: str

    def __init__(self, used_at: str):
        self.used_at = used_at

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'used_at': self.used_at}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(used_at=json['used_at'])


class CodeItemResponse:
    id: str
    code: str
    status: str
    usages: List[CodeUsage]

    def __init__(
        self,
        id: str,
        code: str,
        status: str,
        usages: List[CodeUsage],
    ):
        self.id = id
        self.code = code
        self.status = status
        self.usages = usages

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'code': self.code,
            'status': self.status,
            'usages': [usage.serialize() for usage in self.usages],
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            id=json['id'],
            code=json['code'],
            status=json['status'],
            usages=[CodeUsage.new(usage) for usage in json['usages']],
        )


class CodeListResponse:
    codes: List[CodeItemResponse]
    next_cursor: Optional[str] = None

    def __init__(
        self,
        codes: List[CodeItemResponse],
        next_cursor: Optional[str] = None,
    ):
        self.codes = codes
        self.next_cursor = next_cursor

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'codes': [code.serialize() for code in self.codes]}
        if self.next_cursor is not None:
            data['next_cursor'] = self.next_cursor

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            codes=[CodeItemResponse.new(code) for code in json['codes']],
            next_cursor=json.get('next_cursor'),
        )


class BankName:
    ru: str
    en: str

    def __init__(self, ru: str, en: str):
        self.ru = ru
        self.en = en

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'ru': self.ru, 'en': self.en}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(ru=json['ru'], en=json['en'])


class RawPromocodeGeoRestrictionsPoint:
    corp_geo_id: str
    name: str
    geo: GeoCircle

    def __init__(self, corp_geo_id: str, name: str, geo: GeoCircle):
        self.corp_geo_id = corp_geo_id
        self.name = name
        self.geo = geo

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'corp_geo_id': self.corp_geo_id,
            'name': self.name,
            'geo': self.geo.serialize(),
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            corp_geo_id=json['corp_geo_id'],
            name=json['name'],
            geo=GeoCircle.new(json['geo']),
        )


class RawPromocodeGeoRestrictions:
    source: Optional[RawPromocodeGeoRestrictionsPoint] = None
    destination: Optional[RawPromocodeGeoRestrictionsPoint] = None
    max_intermediate_points: Optional[int] = None

    def __init__(
        self,
        source: Optional[RawPromocodeGeoRestrictionsPoint] = None,
        destination: Optional[RawPromocodeGeoRestrictionsPoint] = None,
        max_intermediate_points: Optional[int] = None,
    ):
        self.source = source
        self.destination = destination
        self.max_intermediate_points = max_intermediate_points

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.source is not None:
            data['source'] = self.source.serialize()
        if self.destination is not None:
            data['destination'] = self.destination.serialize()
        if self.max_intermediate_points is not None:
            data['max_intermediate_points'] = self.max_intermediate_points

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        source = None
        destination = None

        if 'source' in json:
            source = RawPromocodeGeoRestrictionsPoint.new(json['source'])
        if 'destination' in json:
            destination = RawPromocodeGeoRestrictionsPoint.new(json['destination'])

        return cls(
            source=source,
            destination=destination,
            max_intermediate_points=json.get('max_intermediate_points'),
        )


class PromocodeGeoRestrictionsPoint:
    geo_restriction_id: str

    def __init__(self, geo_restriction_id: str):
        self.geo_restriction_id = geo_restriction_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'geo_restriction_id': self.geo_restriction_id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(geo_restriction_id=json['geo_restriction_id'])


class PromocodeGeoRestrictions:
    source: Optional[PromocodeGeoRestrictionsPoint] = None
    destination: Optional[PromocodeGeoRestrictionsPoint] = None
    max_intermediate_points: Optional[int] = None

    def __init__(
        self,
        source: Optional[PromocodeGeoRestrictionsPoint] = None,
        destination: Optional[PromocodeGeoRestrictionsPoint] = None,
        max_intermediate_points: Optional[int] = None,
    ):
        self.source = source
        self.destination = destination
        self.max_intermediate_points = max_intermediate_points

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.source is not None:
            data['source'] = self.source.serialize()
        if self.destination is not None:
            data['destination'] = self.destination.serialize()
        if self.max_intermediate_points is not None:
            data['max_intermediate_points'] = self.max_intermediate_points

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        source = None
        destination = None

        if 'source' in json:
            source = PromocodeGeoRestrictionsPoint.new(json['source'])
        if 'destination' in json:
            destination = PromocodeGeoRestrictionsPoint.new(json['destination'])

        return cls(
            source=source,
            destination=destination,
            max_intermediate_points=json.get('max_intermediate_points'),
        )


class PromocodeOrderPrice:
    cost: str
    cost_with_vat: str
    vat: str
    currency: Optional[str] = None

    def __init__(
        self,
        cost: str,
        cost_with_vat: str,
        vat: str,
        currency: Optional[str] = None,
    ):
        self.cost = cost
        self.cost_with_vat = cost_with_vat
        self.vat = vat
        self.currency = currency

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'cost': self.cost,
            'cost_with_vat': self.cost_with_vat,
            'vat': self.vat,
        }
        if self.currency is not None:
            data['currency'] = self.currency

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            cost=json['cost'],
            cost_with_vat=json['cost_with_vat'],
            vat=json['vat'],
            currency=json.get('currency'),
        )


class PromocodeCreateResponse:
    order_id: str

    def __init__(self, order_id: str):
        self.order_id = order_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'order_id': self.order_id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(order_id=json['order_id'])


class BasePromocodeOrder:
    value: int
    count: int
    active_until: str
    bin_ranges: Optional[List[list]] = None
    bank_name: Optional[BankName] = None
    classes: Optional[List[str]] = None

    def __init__(
        self,
        value: int,
        count: int,
        active_until: str,
        bin_ranges: Optional[List[list]] = None,
        bank_name: Optional[BankName] = None,
        classes: Optional[List[str]] = None,
    ):
        self.value = value
        self.count = count
        self.active_until = active_until
        self.bin_ranges = bin_ranges
        self.bank_name = bank_name
        self.classes = classes

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'count': self.count,
            'value': self.value,
            'active_until': self.active_until,
        }
        if self.bin_ranges is not None:
            data['bin_ranges'] = self.bin_ranges
        if self.bank_name is not None:
            data['bank_name'] = self.bank_name.serialize()
        if self.classes is not None:
            data['classes'] = self.classes
        return data


class Promocode(BasePromocodeOrder):
    name: str
    active_from: Optional[str] = None
    max_usages_count: Optional[int] = None
    service: Optional[PromocodeOrderService] = None
    geo_restrictions: Optional[List[PromocodeGeoRestrictions]] = None

    def __init__(
        self,
        name: str,
        value: int,
        count: int,
        active_until: str,
        bin_ranges: Optional[List[list]] = None,
        bank_name: Optional[BankName] = None,
        geo_restrictions: Optional[List[PromocodeGeoRestrictions]] = None,
        classes: Optional[List[str]] = None,
        active_from: Optional[str] = None,
        max_usages_count: Optional[int] = None,
        service: Optional[PromocodeOrderService] = None,
    ):
        super().__init__(
            value=value,
            count=count,
            active_until=active_until,
            bin_ranges=bin_ranges,
            bank_name=bank_name,
            classes=classes,
        )
        self.name = name
        self.geo_restrictions = geo_restrictions
        self.active_from = active_from
        self.max_usages_count = max_usages_count
        self.service = service

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize(), 'name': self.name}
        if self.active_from is not None:
            data['active_from'] = self.active_from
        if self.max_usages_count is not None:
            data['max_usages_count'] = self.max_usages_count
        if self.service is not None:
            data['service'] = self.service.value
        if self.geo_restrictions is not None:
            data['geo_restrictions'] = [geo.serialize() for geo in self.geo_restrictions]
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        bank_name = None
        geo_restrictions = None
        service = None

        if 'service' in json:
            service = PromocodeOrderService(json['service'])
        if 'bank_name' in json:
            bank_name = BankName.new(json['bank_name'])
        if 'geo_restrictions' in json:
            geo_restrictions = PromocodeGeoRestrictions.new(
                json['geo_restrictions'],
            )

        return cls(
            name=json['name'],
            count=json['count'],
            value=json['value'],
            active_until=json['active_until'],
            bin_ranges=json.get('bin_ranges'),
            bank_name=bank_name,
            geo_restrictions=geo_restrictions,
            classes=json.get('classes'),
            service=service,
            active_from=json.get('active_from'),
            max_usages_count=json.get('max_usages_count'),
        )


class PromocodeOrderResponse(BasePromocodeOrder):
    order_id: str
    status: PromocodeOrderStatus
    pricing: PromocodeOrderPrice
    service: PromocodeOrderService
    geo_restrictions: Optional[List[RawPromocodeGeoRestrictions]] = None

    def __init__(
        self,
        order_id: str,
        value: int,
        count: int,
        status: PromocodeOrderStatus,
        active_until: str,
        pricing: PromocodeOrderPrice,
        service: PromocodeOrderService,
        bin_ranges: Optional[List[list]] = None,
        bank_name: Optional[BankName] = None,
        geo_restrictions: Optional[List[RawPromocodeGeoRestrictions]] = None,
        classes: Optional[List[str]] = None,
    ):
        super().__init__(
            count=count,
            value=value,
            active_until=active_until,
            bin_ranges=bin_ranges,
            bank_name=bank_name,
            classes=classes,
        )
        self.order_id = order_id
        self.status = status
        self.pricing = pricing
        self.service = service
        self.geo_restrictions = geo_restrictions

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'order_id': self.order_id,
            'status': self.status.value,
            'pricing': self.pricing.serialize(),
            'service': self.service.value,
        }
        if self.geo_restrictions is not None:
            data['geo_restrictions'] = [geo.serialize() for geo in self.geo_restrictions]

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        bank_name = None
        geo_restrictions = None

        if 'bank_name' in json:
            bank_name = BankName.new(json['bank_name'])
        if 'geo_restrictions' in json:
            geo_restrictions = [RawPromocodeGeoRestrictions.new(geo) for geo in json['geo_restrictions']]

        return cls(
            order_id=json['order_id'],
            count=json['count'],
            value=json['value'],
            status=PromocodeOrderStatus(json['status']),
            active_until=json['active_until'],
            pricing=PromocodeOrderPrice.new(json['pricing']),
            service=PromocodeOrderService(json['service']),
            bin_ranges=json.get('bin_ranges'),
            bank_name=bank_name,
            geo_restrictions=geo_restrictions,
            classes=json.get('classes'),
        )


class PromocodeOrderListResponse:
    orders: List[PromocodeOrderResponse]
    next_cursor: Optional[str] = None

    def __init__(
        self,
        orders: List[PromocodeOrderResponse],
        next_cursor: Optional[str] = None,
    ):
        self.orders = orders
        self.next_cursor = next_cursor

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'orders': [order.serialize() for order in self.orders]}

        if self.next_cursor is not None:
            data['next_cursor'] = self.next_cursor

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            orders=[PromocodeOrderResponse.new(order) for order in json['orders']],
            next_cursor=json.get('next_cursor'),
        )


class PromocodeOrderCancelResponse:
    status: PromocodeOrderCancelStatus

    def __init__(self, status: PromocodeOrderCancelStatus):
        self.status = status

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'status': self.status.value}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(status=PromocodeOrderCancelStatus(json['status']))


class TankerOrderItemResponse:
    id: str
    user_id: str
    client_id: str
    created_at: str
    closed_at: Optional[str] = None
    fuel_type: Optional[str] = None
    final_price: Optional[str] = None
    liters_filled: Optional[str] = None
    station_location: Optional[List[float]] = None

    def __init__(
        self,
        id: str,
        user_id: str,
        client_id: str,
        created_at: str,
        closed_at: Optional[str] = None,
        fuel_type: Optional[str] = None,
        final_price: Optional[str] = None,
        liters_filled: Optional[str] = None,
        station_location: Optional[List[float]] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.client_id = client_id
        self.created_at = created_at
        self.closed_at = closed_at
        self.fuel_type = fuel_type
        self.final_price = final_price
        self.liters_filled = liters_filled
        self.station_location = station_location

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'user_id': self.user_id,
            'client_id': self.client_id,
            'created_at': self.created_at,
        }

        if self.closed_at is not None:
            data['closed_at'] = self.closed_at
        if self.fuel_type is not None:
            data['fuel_type'] = self.fuel_type
        if self.final_price is not None:
            data['final_price'] = self.final_price
        if self.liters_filled is not None:
            data['liters_filled'] = self.liters_filled
        if self.station_location is not None:
            data['station_location'] = self.station_location

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            id=json['id'],
            user_id=json['user_id'],
            client_id=json['client_id'],
            created_at=json['created_at'],
            closed_at=json.get('closed_at'),
            fuel_type=json.get('fuel_type'),
            final_price=json.get('final_price'),
            liters_filled=json.get('liters_filled'),
            station_location=json.get('station_location'),
        )


class TankerOrdersResponse:
    orders: List[TankerOrderItemResponse]
    last_closed_at: Optional[str] = None

    def __init__(
        self,
        orders: List[TankerOrderItemResponse],
        last_closed_at: Optional[str] = None,
    ):
        self.orders = orders
        self.last_closed_at = last_closed_at

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'orders': [order.serialize() for order in self.orders],
        }
        if self.last_closed_at is not None:
            data['last_closed_at'] = self.last_closed_at

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            orders=[TankerOrderItemResponse.new(order) for order in json['orders']],
            last_closed_at=json.get('last_closed_at'),
        )


class BaseManager:
    yandex_login: str
    role: Role
    email: Optional[str] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[str] = None

    def __init__(
        self,
        yandex_login: str,
        role: Role,
        email: Optional[str] = None,
        fullname: Optional[str] = None,
        phone: Optional[str] = None,
        department_id: Optional[str] = None,
    ):
        self.yandex_login = yandex_login
        self.role = role
        self.email = email
        self.fullname = fullname
        self.phone = phone
        self.department_id = department_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'yandex_login': self.yandex_login,
            'role': self.role.value,
        }
        if self.department_id is not None:
            data['department_id'] = self.department_id
        if self.email is not None:
            data['email'] = self.email
        if self.fullname is not None:
            data['fullname'] = self.fullname
        if self.phone is not None:
            data['phone'] = self.phone
        return data


class Manager(BaseManager):
    email: str
    fullname: str
    phone: str
    yandex_login: str
    role: Role
    department_id: Optional[str] = None

    def __init__(
        self,
        email: str,
        fullname: str,
        phone: str,
        yandex_login: str,
        role: Role,
        department_id: Optional[str] = None,
    ):
        if not isinstance(email, str):
            raise ValidationError(error_string('email', email, 'str'))
        if not isinstance(fullname, str):
            raise ValidationError(error_string('fullname', fullname, 'str'))
        if not isinstance(phone, str):
            raise ValidationError(error_string('phone', phone, 'str'))
        if not isinstance(yandex_login, str):
            raise ValidationError(error_string('yandex_login', yandex_login, 'str'))
        if not isinstance(role, Role):
            raise ValidationError(error_string('role', role, 'Role'))
        if department_id is not None:
            if not isinstance(department_id, str):
                raise ValidationError(error_string('department_id', department_id, 'str'))
        super().__init__(
            email=email,
            fullname=fullname,
            phone=phone,
            yandex_login=yandex_login,
            role=role,
            department_id=department_id,
        )

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}

        return data


class ManagerItemResponse(BaseManager):
    id: str

    def __init__(
        self,
        yandex_login: str,
        role: Role,
        id: str,
        email: Optional[str] = None,
        fullname: Optional[str] = None,
        phone: Optional[str] = None,
        department_id: Optional[str] = None,
    ):
        super().__init__(
            email=email,
            fullname=fullname,
            phone=phone,
            yandex_login=yandex_login,
            role=role,
            department_id=department_id,
        )
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize(), 'id': self.id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            email=json.get('email'),
            fullname=json.get('fullname'),
            phone=json.get('phone'),
            yandex_login=json['yandex_login'],
            role=Role(json['role']),
            id=json['id'],
            department_id=json.get('department_id'),
        )


class ManagersListResponse:
    items: List[ManagerItemResponse]
    limit: int
    total_amount: int
    cursor: Optional[str] = None
    next_cursor: Optional[str] = None

    def __init__(
        self,
        items: List[ManagerItemResponse],
        limit: int,
        total_amount: int,
        cursor: Optional[str] = None,
        next_cursor: Optional[str] = None,
    ):
        self.items = items
        self.limit = limit
        self.total_amount = total_amount
        self.cursor = cursor
        self.next_cursor = next_cursor

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [role.serialize() for role in self.items],
            'limit': self.limit,
            'total_amount': self.total_amount,
        }

        if self.cursor is not None:
            data['cursor'] = self.cursor
        if self.next_cursor is not None:
            data['next_cursor'] = self.next_cursor

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[ManagerItemResponse.new(role) for role in json['items']],
            limit=json['limit'],
            total_amount=json['total_amount'],
            cursor=json.get('cursor'),
            next_cursor=json.get('next_cursor'),
        )


class ManagerResponse:
    id: str

    def __init__(self, id: str):
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'id': self.id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['id'])


class Limit:
    limit_id: str
    service: Service
    is_fleet_limit: Optional[bool] = None

    def __init__(
        self,
        limit_id: str,
        service: Service,
        is_fleet_limit: Optional[bool] = None,
    ):
        if not isinstance(limit_id, str):
            raise ValidationError(error_string('limit_id', limit_id, 'str'))
        self.limit_id = limit_id
        if not isinstance(service, Service):
            raise ValidationError(error_string('service', service, 'Service'))
        self.service = service
        if is_fleet_limit is not None:
            if not isinstance(is_fleet_limit, bool):
                raise ValidationError(error_string('is_fleet_limit', is_fleet_limit, 'bool'))
        self.is_fleet_limit = is_fleet_limit

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'limit_id': self.limit_id,
            'service': self.service.value,
        }
        if self.is_fleet_limit is not None:
            data['is_fleet_limit'] = self.is_fleet_limit

        return data


class User:
    fullname: str
    phone: str
    is_active: bool
    email: Optional[str] = None
    cost_center: Optional[str] = None
    cost_centers_id: Optional[str] = None
    nickname: Optional[str] = None
    department_id: Optional[str] = None
    limits: Optional[List[Limit]] = None

    def __init__(
        self,
        fullname: str,
        phone: str,
        is_active: bool,
        email: Optional[str] = None,
        cost_center: Optional[str] = None,
        cost_centers_id: Optional[str] = None,
        nickname: Optional[str] = None,
        department_id: Optional[str] = None,
        limits: Optional[List[Limit]] = None,
    ):
        if not isinstance(fullname, str):
            raise ValidationError(error_string('fullname', fullname, 'str'))
        self.fullname = fullname
        if not isinstance(phone, str):
            raise ValidationError(error_string('phone', phone, 'str'))
        self.phone = phone
        if not isinstance(is_active, bool):
            raise ValidationError(error_string('is_active', is_active, 'bool'))
        self.is_active = is_active
        if email is not None:
            if not isinstance(email, str):
                raise ValidationError(error_string('email', email, 'str'))
        self.email = email
        if cost_center is not None:
            if not isinstance(cost_center, str):
                raise ValidationError(error_string('cost_center', cost_center, 'str'))
        self.cost_center = cost_center
        if cost_centers_id is not None:
            if not isinstance(cost_centers_id, str):
                raise ValidationError(error_string('cost_centers_id', cost_centers_id, 'str'))
        self.cost_centers_id = cost_centers_id
        if nickname is not None:
            if not isinstance(nickname, str):
                raise ValidationError(error_string('nickname', nickname, 'str'))
        self.nickname = nickname
        if department_id is not None:
            if not isinstance(department_id, str):
                raise ValidationError(error_string('department_id', department_id, 'str'))
        self.department_id = department_id
        if limits is not None:
            if not isinstance(limits, List):
                raise ValidationError(error_string('limits', limits, 'List'))
            for limit in limits:
                if not isinstance(limit, Limit):
                    raise ValidationError(error_string('limit', limit, 'Limit'))
        self.limits = limits

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'fullname': self.fullname,
            'phone': self.phone,
            'is_active': self.is_active,
        }
        if self.cost_centers_id is not None:
            data['cost_centers_id'] = self.cost_centers_id
        if self.nickname is not None:
            data['nickname'] = self.nickname
        if self.department_id is not None:
            data['department_id'] = self.department_id
        if self.limits is not None:
            data['limits'] = [limit.serialize() for limit in self.limits]
        if self.email is not None:
            data['email'] = self.email
        if self.cost_center is not None:
            data['cost_center'] = self.cost_center

        return data


class UserGetResponse(User):
    id: str
    is_deleted: bool
    client_id: Optional[str] = None

    def __init__(
        self,
        fullname: str,
        phone: str,
        is_active: bool,
        id: str,
        is_deleted: bool,
        client_id: Optional[str] = None,
        email: Optional[str] = None,
        cost_center: Optional[str] = None,
        cost_centers_id: Optional[str] = None,
        nickname: Optional[str] = None,
        department_id: Optional[str] = None,
        limits: Optional[List[Limit]] = None,
    ):
        super().__init__(
            fullname=fullname,
            phone=phone,
            is_active=is_active,
            email=email,
            cost_center=cost_center,
            cost_centers_id=cost_centers_id,
            nickname=nickname,
            department_id=department_id,
            limits=limits,
        )
        self.id = id
        self.is_deleted = is_deleted
        self.client_id = client_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'id': self.id,
            'is_deleted': self.is_deleted,
        }
        if self.client_id is not None:
            data['client_id'] = self.client_id

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        limits = None
        if 'limits' in json:
            limits = [
                Limit(
                    limit_id=limit['limit_id'],
                    service=Service(limit['service']),
                    is_fleet_limit=limit.get('is_fleet_limit'),
                )
                for limit in json['limits']
            ]

        return cls(
            fullname=json['fullname'],
            phone=json['phone'],
            is_active=json['is_active'],
            id=json['id'],
            is_deleted=json['is_deleted'],
            client_id=json.get('client_id'),
            email=json.get('email'),
            cost_center=json.get('cost_center'),
            cost_centers_id=json.get('cost_centers_id'),
            nickname=json.get('nickname'),
            department_id=json.get('department_id'),
            limits=limits,
        )


class UserCreateResponse:
    id: str

    def __init__(self, id: str):
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'id': self.id}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['id'])


class UserUpdateResponse:
    status: str

    def __init__(self, status: str):
        self.status = status

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'status': self.status}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(status=json['status'])


class UserListResponse:
    items: List[UserGetResponse]
    limit: int
    total_amount: int
    cursor: Optional[str] = None
    next_cursor: Optional[str] = None

    def __init__(
        self,
        items: List[UserGetResponse],
        limit: int,
        total_amount: int,
        cursor: Optional[str] = None,
        next_cursor: Optional[str] = None,
    ):
        self.items = items
        self.limit = limit
        self.total_amount = total_amount
        self.cursor = cursor
        self.next_cursor = next_cursor

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [user.serialize() for user in self.items],
            'limit': self.limit,
            'total_amount': self.total_amount,
        }

        if self.cursor is not None:
            data['cursor'] = self.cursor
        if self.next_cursor is not None:
            data['next_cursor'] = self.next_cursor

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[UserGetResponse.new(user) for user in json['items']],
            limit=json['limit'],
            total_amount=json['total_amount'],
            cursor=json.get('cursor'),
            next_cursor=json.get('next_cursor'),
        )


class UsersSpendingListRequest:
    user_ids: List[str]

    def __init__(self, user_ids: List[str]):
        if len(user_ids) > 100:
            user_ids = user_ids[:100]
        self.user_ids = user_ids

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'user_ids': self.user_ids}
        return data


class LimitSpendingDetailsResponse:
    orders_cost: Optional[str] = None
    spent: Optional[str] = None
    orders_amount: Optional[int] = None
    orders_spent: Optional[int] = None

    def __init__(
        self,
        orders_cost: Optional[str] = None,
        spent: Optional[str] = None,
        orders_amount: Optional[int] = None,
        orders_spent: Optional[int] = None,
    ):
        self.orders_cost = orders_cost
        self.spent = spent
        self.orders_amount = orders_amount
        self.orders_spent = orders_spent

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.orders_cost is not None:
            data['orders_cost'] = self.orders_cost
        if self.spent is not None:
            data['spent'] = self.spent
        if self.orders_amount is not None:
            data['orders_amount'] = self.orders_amount
        if self.orders_spent is not None:
            data['orders_spent'] = self.orders_spent

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            orders_cost=json.get('orders_cost'),
            spent=json.get('spent'),
            orders_amount=json.get('orders_amount'),
            orders_spent=json.get('orders_spent'),
        )


class UserSpendingLimitItemResponse(Limit):
    spending_details: LimitSpendingDetailsResponse

    def __init__(
        self,
        limit_id: str,
        service: Service,
        spending_details: LimitSpendingDetailsResponse,
    ):
        super().__init__(limit_id=limit_id, service=service)
        self.spending_details = spending_details

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'spending_details': self.spending_details.serialize(),
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            limit_id=json['limit_id'],
            service=Service(json['service']),
            spending_details=LimitSpendingDetailsResponse.new(
                json['spending_details'],
            ),
        )


class UserSpendingItemResponse:
    user_id: str
    limits: List[UserSpendingLimitItemResponse]

    def __init__(
        self,
        user_id: str,
        limits: List[UserSpendingLimitItemResponse],
    ):
        self.user_id = user_id
        self.limits = limits

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'user_id': self.user_id,
            'limits': [limit.serialize() for limit in self.limits],
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            user_id=json['user_id'],
            limits=[UserSpendingLimitItemResponse.new(limit) for limit in json['limits']],
        )


class UsersSpendingListResponse:
    users: List[UserSpendingItemResponse]

    def __init__(self, users: List[UserSpendingItemResponse]):
        self.users = users

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'users': [user.serialize() for user in self.users],
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            users=[UserSpendingItemResponse.new(user) for user in json['users']],
        )


class Measure:
    value: int
    period: MeasurePeriod
    kind: Optional[MeasureKind] = None

    def __init__(
        self,
        value: int,
        period: MeasurePeriod,
        kind: Optional[MeasureKind] = None,
    ):
        self.value = value
        self.period = period
        self.kind = kind

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'value': self.value,
            'period': self.period.value,
        }
        if self.kind is not None:
            data['kind'] = self.kind.value

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        kind = None
        if 'kind' in json:
            kind = MeasureKind(json['kind'])

        return cls(
            value=json['value'],
            period=MeasurePeriod(json['period']),
            kind=kind,
        )


class Limits:
    orders_cost: Measure
    orders_amount: Optional[Measure] = None

    def __init__(
        self,
        orders_cost: Measure,
        orders_amount: Optional[Measure] = None,
    ):
        self.orders_cost = orders_cost
        self.orders_amount = orders_amount

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'orders_cost': self.orders_cost.serialize()}
        if self.orders_amount is not None:
            data['orders_amount'] = self.orders_amount.serialize()

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        orders_amount = None
        if 'orders_amount' in json:
            orders_amount = Measure.new(json['orders_amount'])
        return cls(
            orders_cost=Measure.new(json['orders_cost']),
            orders_amount=orders_amount,
        )


class GeoRestriction:
    source: Optional[str]
    destination: Optional[str]
    prohibiting_restriction: bool

    def __init__(
        self,
        source: Optional[str],
        destination: Optional[str],
        prohibiting_restriction: bool,
    ):
        self.source = source
        self.destination = destination
        self.prohibiting_restriction = prohibiting_restriction

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'prohibiting_restriction': self.prohibiting_restriction,
        }
        if self.source is not None:
            data['source'] = self.source
        if self.destination is not None:
            data['destination'] = self.destination

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            source=json.get('source'),
            destination=json.get('destination'),
            prohibiting_restriction=json['prohibiting_restriction'],
        )


class TimeRestriction:
    type: TimeRestrictionType
    days: Optional[List[Day]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    def __init__(
        self,
        type: TimeRestrictionType,
        days: Optional[List[Day]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        self.type = type
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'type': self.type.value}
        if self.days is not None:
            data['days'] = [day.value for day in self.days]
        if self.start_time is not None:
            data['start_time'] = self.start_time
        if self.end_time is not None:
            data['end_time'] = self.end_time
        if self.start_date is not None:
            data['start_date'] = self.start_date
        if self.end_date is not None:
            data['end_date'] = self.end_date

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        days = None
        if 'days' in json:
            days = [Day(day) for day in json['days']]

        return cls(
            type=TimeRestrictionType(json['type']),
            days=days,
            start_time=json.get('start_time'),
            end_time=json.get('end_time'),
            start_date=json.get('start_date'),
            end_date=json.get('end_date'),
        )


class Counter:
    users: int

    def __init__(self, users: int):
        self.users = users

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'users': self.users}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(users=json['users'])


class BudgetLimit:
    title: str
    client_id: str
    service: Service
    department_id: Optional[str] = None
    categories: Optional[List[str]] = None
    fuel_types: Optional[List[str]] = None
    limits: Optional[Limits] = None
    geo_restrictions: Optional[List[GeoRestriction]] = None
    time_restrictions: Optional[List[TimeRestriction]] = None
    can_edit: Optional[bool] = None
    counters: Optional[Counter] = None
    is_default: Optional[bool] = None
    is_qr_enabled: Optional[bool] = None
    cities: Optional[List[str]] = None
    tariffs: Optional[List[str]] = None
    car_classes: Optional[List[str]] = None
    enable_toll_roads: Optional[str] = None

    def __init__(
        self,
        title: str,
        client_id: str,
        service: Service,
        department_id: Optional[str] = None,
        categories: Optional[List[str]] = None,
        fuel_types: Optional[List[str]] = None,
        limits: Optional[Limits] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        can_edit: Optional[bool] = None,
        counters: Optional[Counter] = None,
        is_default: Optional[bool] = None,
        is_qr_enabled: Optional[bool] = None,
        cities: Optional[List[str]] = None,
        tariffs: Optional[List[str]] = None,
        car_classes: Optional[List[str]] = None,
        enable_toll_roads: Optional[str] = None,
    ):
        self.title = title
        self.client_id = client_id
        self.service = service
        self.department_id = department_id
        self.categories = categories
        self.fuel_types = fuel_types
        self.limits = limits
        self.geo_restrictions = geo_restrictions
        self.time_restrictions = time_restrictions
        self.can_edit = can_edit
        self.counters = counters
        self.is_default = is_default
        self.is_qr_enabled = is_qr_enabled
        self.cities = cities
        self.tariffs = tariffs
        self.car_classes = car_classes
        self.enable_toll_roads = enable_toll_roads

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'title': self.title,
            'client_id': self.client_id,
            'service': self.service.value,
        }
        if self.department_id is not None:
            data['department_id'] = self.department_id
        if self.categories is not None:
            data['categories'] = self.categories
        if self.fuel_types is not None:
            data['fuel_types'] = self.fuel_types
        if self.limits is not None:
            data['limits'] = self.limits
        if self.geo_restrictions is not None:
            data['geo_restrictions'] = self.geo_restrictions
        if self.time_restrictions is not None:
            data['time_restrictions'] = self.time_restrictions
        if self.can_edit is not None:
            data['can_edit'] = self.can_edit
        if self.counters is not None:
            data['counters'] = self.counters
        if self.is_default is not None:
            data['is_default'] = self.is_default
        if self.is_qr_enabled is not None:
            data['is_qr_enabled'] = self.is_qr_enabled
        if self.cities is not None:
            data['cities'] = self.cities
        if self.tariffs is not None:
            data['tariffs'] = self.tariffs
        if self.car_classes is not None:
            data['car_classes'] = self.car_classes
        if self.enable_toll_roads is not None:
            data['enable_toll_roads'] = self.enable_toll_roads

        return data


class BudgetLimitRequest:
    title: str
    limits: Limits
    service: Service
    client_id: Optional[str] = None
    department_id: Optional[str] = None
    time_restrictions: Optional[List[TimeRestriction]] = None
    geo_restrictions: Optional[List[GeoRestriction]] = None

    def __init__(
        self,
        title: str,
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
    ):
        self.title = title
        self.limits = limits
        self.service = service
        self.client_id = client_id
        self.department_id = department_id
        self.time_restrictions = time_restrictions
        self.geo_restrictions = geo_restrictions

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'title': self.title,
            'limits': self.limits,
            'service': self.service.value,
        }
        if self.client_id is not None:
            data['client_id'] = self.client_id
        if self.department_id is not None:
            data['department_id'] = self.department_id
        if self.time_restrictions is not None:
            data['time_restrictions'] = self.time_restrictions
        if self.geo_restrictions is not None:
            data['geo_restrictions'] = self.geo_restrictions

        return data


class BudgetLimitTaxiRequest(BudgetLimitRequest):
    categories: List[str]
    enable_toll_roads: Optional[str] = None

    def __init__(
        self,
        title: str,
        categories: List[str],
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
        enable_toll_roads: Optional[str] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
            time_restrictions=time_restrictions,
            geo_restrictions=geo_restrictions,
        )
        self.categories = categories
        self.enable_toll_roads = enable_toll_roads

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'categories': self.categories,
        }
        if self.enable_toll_roads is not None:
            data['enable_toll_roads'] = self.enable_toll_roads

        return data


class BudgetLimitEatsRequest(BudgetLimitRequest):
    is_qr_enabled: Optional[str] = None

    def __init__(
        self,
        title: str,
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
        is_qr_enabled: Optional[str] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
            time_restrictions=time_restrictions,
            geo_restrictions=geo_restrictions,
        )
        self.is_qr_enabled = is_qr_enabled

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.is_qr_enabled is not None:
            data['is_qr_enabled'] = self.is_qr_enabled

        return data


class BudgetLimitTankerRequest(BudgetLimitRequest):
    fuel_types: Optional[List[str]] = None

    def __init__(
        self,
        title: str,
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
        fuel_types: Optional[List[str]] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
            time_restrictions=time_restrictions,
            geo_restrictions=geo_restrictions,
        )
        self.fuel_types = fuel_types

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.fuel_types is not None:
            data['fuel_types'] = self.fuel_types

        return data


class BudgetLimitDriveRequest(BudgetLimitRequest):
    cities: Optional[List[str]] = None
    tariffs: Optional[List[str]] = None
    cars_classes: Optional[List[str]] = None
    insurance_types: Optional[List[str]] = None
    enable_toll_roads: Optional[bool] = None

    def __init__(
        self,
        title: str,
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        cities: Optional[List[str]] = None,
        tariffs: Optional[List[str]] = None,
        cars_classes: Optional[List[str]] = None,
        insurance_types: Optional[List[str]] = None,
        enable_toll_roads: Optional[bool] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
            time_restrictions=time_restrictions,
        )
        self.cities = cities
        self.tariffs = tariffs
        self.cars_classes = cars_classes
        self.insurance_types = insurance_types
        self.enable_toll_roads = enable_toll_roads

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.cities is not None:
            data['cities'] = self.cities
        if self.tariffs is not None:
            data['tariffs'] = self.tariffs
        if self.cars_classes is not None:
            data['cars_classes'] = self.cars_classes
        if self.insurance_types is not None:
            data['insurance_types'] = self.insurance_types
        if self.enable_toll_roads is not None:
            data['enable_toll_roads'] = self.enable_toll_roads

        return data


class BudgetLimitGroceryRequest(BudgetLimitRequest):
    def __init__(
        self,
        title: str,
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
            time_restrictions=time_restrictions,
            geo_restrictions=geo_restrictions,
        )

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}

        return data


class BudgetLimitCargoRequest(BudgetLimitRequest):
    categories: List[str]

    def __init__(
        self,
        title: str,
        categories: List[str],
        limits: Limits,
        service: Service,
        client_id: Optional[str] = None,
        department_id: Optional[str] = None,
    ):
        super().__init__(
            title=title,
            limits=limits,
            service=service,
            client_id=client_id,
            department_id=department_id,
        )
        self.categories = categories

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'categories': self.categories,
        }

        return data


class GeoHotelPolicy:
    geo_id: int
    name: str
    type: GeoHotelPolicyType
    max_price_per_day: Optional[int] = None
    min_price_per_day: Optional[int] = None

    def __init__(
        self,
        geo_id: int,
        name: str,
        type: GeoHotelPolicyType,
        max_price_per_day: Optional[int] = None,
        min_price_per_day: Optional[int] = None,
    ):
        if not isinstance(type, GeoHotelPolicyType):
            raise ValidationError(error_string('type', type, 'GeoHotelPolicyType'))
        self.type = type
        self.geo_id = geo_id
        self.name = name
        self.max_price_per_day = max_price_per_day
        self.min_price_per_day = min_price_per_day

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'geo_id': self.geo_id,
            'name': self.name,
            'type': self.type.value,
        }

        if self.max_price_per_day is not None:
            data['max_price_per_day'] = self.max_price_per_day
        if self.min_price_per_day is not None:
            data['min_price_per_day'] = self.min_price_per_day

        return data


class HotelPolicy:
    geo: Optional[GeoHotelPolicy] = None
    stars: Optional[List[int]] = None
    max_price_per_day: Optional[int] = None
    min_price_per_day: Optional[int] = None
    weekly_restrictions: Optional[List[Day]] = None

    def __init__(
        self,
        geo: Optional[GeoHotelPolicy] = None,
        stars: Optional[List[int]] = None,
        max_price_per_day: Optional[int] = None,
        min_price_per_day: Optional[int] = None,
        weekly_restrictions: Optional[List[Day]] = None,
    ):
        self.geo = geo
        self.stars = stars
        self.max_price_per_day = max_price_per_day
        self.min_price_per_day = min_price_per_day
        self.weekly_restrictions = weekly_restrictions

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.geo is not None:
            data['geo'] = self.geo.serialize()
        if self.stars is not None:
            data['stars'] = self.stars
        if self.max_price_per_day is not None:
            data['max_price_per_day'] = self.max_price_per_day
        if self.min_price_per_day is not None:
            data['min_price_per_day'] = self.min_price_per_day
        if self.weekly_restrictions is not None:
            data['weekly_restrictions'] = [day.value for day in self.weekly_restrictions]

        return data


class AviaPolicy:
    max_price: Optional[int] = None
    min_price: Optional[int] = None
    countries_restrictions: Optional[List[CountriesRestriction]] = None
    classes: Optional[List[TravelClass]] = None
    extra_baggage: Optional[bool] = None
    aeroexpress: Optional[bool] = None

    def __init__(
        self,
        max_price: Optional[int] = None,
        min_price: Optional[int] = None,
        countries_restrictions: Optional[List[CountriesRestriction]] = None,
        classes: Optional[List[TravelClass]] = None,
        extra_baggage: Optional[bool] = None,
        aeroexpress: Optional[bool] = None,
    ):
        self.max_price = max_price
        self.min_price = min_price
        self.countries_restrictions = countries_restrictions
        self.classes = classes
        self.extra_baggage = extra_baggage
        self.aeroexpress = aeroexpress

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.max_price is not None:
            data['max_price'] = self.max_price
        if self.min_price is not None:
            data['min_price'] = self.min_price
        if self.countries_restrictions is not None:
            data['countries_restrictions'] = [item.value for item in self.countries_restrictions]
        if self.classes is not None:
            data['classes'] = [item.value for item in self.classes]
        if self.extra_baggage is not None:
            data['extra_baggage'] = self.extra_baggage
        if self.aeroexpress is not None:
            data['aeroexpress'] = self.aeroexpress

        return data


class BudgetLimitTravelRequest(BudgetLimitRequest):
    service: Service
    title: str
    limits: Limits
    department_id: Optional[str] = None
    client_id: Optional[str] = None
    hotel_policy: Optional[HotelPolicy] = None
    avia_policy: Optional[AviaPolicy] = None
    allow_reservations_without_approve: Optional[bool] = None
    approve_role: Optional[ApproveRole] = None
    approve_roles: Optional[List[ApproveRole]] = None

    def __init__(
        self,
        service: Service,
        title: str,
        limits: Limits,
        department_id: Optional[str] = None,
        client_id: Optional[str] = None,
        hotel_policy: Optional[HotelPolicy] = None,
        avia_policy: Optional[AviaPolicy] = None,
        allow_reservations_without_approve: Optional[bool] = None,
        approve_role: Optional[ApproveRole] = None,
        approve_roles: Optional[List[ApproveRole]] = None,
    ):
        super().__init__(service=service, title=title, limits=limits, department_id=department_id, client_id=client_id)
        self.hotel_policy = hotel_policy
        self.avia_policy = avia_policy
        self.allow_reservations_without_approve = allow_reservations_without_approve
        self.approve_role = approve_role
        self.approve_roles = approve_roles

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.hotel_policy is not None:
            data['hotel_policy'] = self.hotel_policy.serialize()
        if self.avia_policy is not None:
            data['avia_policy'] = self.avia_policy.serialize()
        if self.allow_reservations_without_approve is not None:
            data['allow_reservations_without_approve'] = self.allow_reservations_without_approve
        if self.approve_role is not None:
            data['approve_role'] = self.approve_role.value
        if self.approve_roles is not None:
            data['approve_roles'] = [item.value for item in self.approve_roles]

        return data


class BudgetLimitItemResponse(BudgetLimit):
    id: str

    def __init__(
        self,
        title: str,
        client_id: str,
        service: Service,
        id: str,
        department_id: Optional[str] = None,
        categories: Optional[List[str]] = None,
        fuel_types: Optional[List[str]] = None,
        limits: Optional[Limits] = None,
        geo_restrictions: Optional[List[GeoRestriction]] = None,
        time_restrictions: Optional[List[TimeRestriction]] = None,
        can_edit: Optional[bool] = None,
        counters: Optional[Counter] = None,
        is_default: Optional[bool] = None,
        is_qr_enabled: Optional[bool] = None,
        cities: Optional[List[str]] = None,
        tariffs: Optional[List[str]] = None,
        car_classes: Optional[List[str]] = None,
        enable_toll_roads: Optional[str] = None,
    ):
        super().__init__(
            title=title,
            client_id=client_id,
            service=service,
            department_id=department_id,
            categories=categories,
            fuel_types=fuel_types,
            limits=limits,
            geo_restrictions=geo_restrictions,
            time_restrictions=time_restrictions,
            can_edit=can_edit,
            counters=counters,
            is_default=is_default,
            is_qr_enabled=is_qr_enabled,
            cities=cities,
            tariffs=tariffs,
            car_classes=car_classes,
            enable_toll_roads=enable_toll_roads,
        )
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize(), 'id': self.id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        geo_restrictions = None
        if 'geo_restrictions' in json:
            geo_restrictions = [GeoRestriction.new(geo) for geo in json['geo_restrictions']]
        time_restrictions = None
        if 'time_restrictions' in json:
            time_restrictions = [TimeRestriction.new(time) for time in json['time_restrictions']]
        return cls(
            title=json['title'],
            client_id=json['client_id'],
            service=Service(json['service']),
            id=json['id'],
            department_id=json.get('department_id'),
            categories=json.get('categories'),
            fuel_types=json.get('fuel_types'),
            limits=json.get('limits'),
            geo_restrictions=geo_restrictions,
            time_restrictions=time_restrictions,
            can_edit=json.get('can_edit'),
            counters=json.get('counters'),
            is_default=json.get('is_default'),
            is_qr_enabled=json.get('is_qr_enabled'),
            cities=json.get('cities'),
            tariffs=json.get('tariffs'),
            car_classes=json.get('car_classes'),
            enable_toll_roads=json.get('enable_toll_roads'),
        )


class BudgetLimitListResponse:
    items: List[BudgetLimitItemResponse]
    limit: int
    offset: int
    total_amount: int

    def __init__(
        self,
        items: List[BudgetLimitItemResponse],
        limit: int,
        offset: int,
        total_amount: int,
    ):
        self.items = items
        self.limit = limit
        self.offset = offset
        self.total_amount = total_amount

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [limit.serialize() for limit in self.items],
            'limit': self.limit,
            'offset': self.offset,
            'total_amount': self.total_amount,
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[BudgetLimitItemResponse.new(limit) for limit in json['items']],
            limit=json['limit'],
            offset=json['offset'],
            total_amount=json['total_amount'],
        )


class BudgetLimitUpdateResponse:
    id: str

    def __init__(self, id: str):
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'id': self.id}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['id'])


class FieldSetting:
    title: str
    required: bool
    services: List[Service]
    format: CostCenterFormat
    values: List[str]
    id: Optional[str] = None
    hidden: Optional[bool] = None

    def __init__(
        self,
        title: str,
        required: bool,
        services: List[Service],
        format: CostCenterFormat,
        values: List[str],
        id: Optional[str] = None,
        hidden: Optional[bool] = None,
    ):
        self.id = id
        self.hidden = hidden
        self.title = title
        self.required = required
        self.services = services
        self.format = format
        self.values = values

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'title': self.title,
            'required': self.required,
            'services': [service.value for service in self.services],
            'format': self.format.value,
            'values': self.values,
        }
        if self.id is not None:
            data['id'] = self.id
        if self.hidden is not None:
            data['hidden'] = self.hidden

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            id=json.get('id'),
            hidden=json.get('hidden'),
            title=json['title'],
            required=json['required'],
            services=[Service(service) for service in json['services']],
            format=CostCenterFormat(json['format']),
            values=json['values'],
        )


class BudgetCostCenterItemResponse:
    id: Optional[str] = None
    name: Optional[str] = None
    default: Optional[bool] = None
    field_settings: Optional[List[FieldSetting]] = None

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        default: Optional[bool] = None,
        field_settings: Optional[List[FieldSetting]] = None,
    ):
        self.id = id
        self.name = name
        self.default = default
        self.field_settings = field_settings

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.id is not None:
            data['id'] = self.id
        if self.name is not None:
            data['name'] = self.name
        if self.default is not None:
            data['default'] = self.default
        if self.field_settings is not None:
            data['field_settings'] = [field.serialize() for field in self.field_settings]
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        field_settings = None
        if 'field_settings' in json:
            field_settings = [FieldSetting.new(setting) for setting in json['field_settings']]
        return cls(
            id=json.get('id'),
            name=json.get('name'),
            default=json.get('default'),
            field_settings=field_settings,
        )


class BudgetCostCenterListResponse:
    items: List[BudgetCostCenterItemResponse]
    limit: int
    offset: int
    total_amount: int

    def __init__(
        self,
        items: List[BudgetCostCenterItemResponse],
        limit: int,
        offset: int,
        total_amount: int,
    ):
        self.items = items
        self.limit = limit
        self.offset = offset
        self.total_amount = total_amount

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [cost_center.serialize() for cost_center in self.items],
            'limit': self.limit,
            'offset': self.offset,
            'total_amount': self.total_amount,
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[BudgetCostCenterItemResponse.new(cost_center) for cost_center in json['items']],
            limit=json['limit'],
            offset=json['offset'],
            total_amount=json['total_amount'],
        )


class Department:
    name: str
    parent_id: Optional[str] = None

    def __init__(self, name: str, parent_id: Optional[str] = None):
        self.name = name
        self.parent_id = parent_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'name': self.name, 'parent_id': self.parent_id}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(name=json['name'], parent_id=json['parent_id'])


class DepartmentCreateResponse:
    id: str

    def __init__(self, id):
        self.id = id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'_id': self.id}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(id=json['_id'])


class DepartmentBudget:
    budget: Optional[Union[float, int, Decimal]] = None

    def __init__(self, budget: Optional[Union[float, int, Decimal]] = None):
        self.budget = budget

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'budget': self.budget}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(budget=json['budget'])


class DepartmentLimits:
    taxi: DepartmentBudget
    eats: DepartmentBudget
    tanker: DepartmentBudget
    cargo: DepartmentBudget

    def __init__(
        self,
        taxi: DepartmentBudget,
        eats: DepartmentBudget,
        tanker: DepartmentBudget,
        cargo: DepartmentBudget,
    ):
        self.taxi = taxi
        self.eats = eats
        self.tanker = tanker
        self.cargo = cargo

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'taxi': self.taxi.serialize(),
            'eats2': self.eats.serialize(),
            'tanker': self.tanker.serialize(),
            'cargo': self.cargo.serialize(),
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            taxi=DepartmentBudget.new(json['taxi']),
            eats=DepartmentBudget.new(json['eats2']),
            tanker=DepartmentBudget.new(json['tanker']),
            cargo=DepartmentBudget.new(json['cargo']),
        )


class DepartmentItemResponse(Department):
    id: str
    limits: DepartmentLimits

    def __init__(
        self,
        name: str,
        id: str,
        limits: DepartmentLimits,
        parent_id: Optional[str] = None,
    ):
        super().__init__(name=name, parent_id=parent_id)
        self.id = id
        self.limits = limits

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            **super().serialize(),
            'id': self.id,
            'limits': self.limits.serialize(),
        }
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            name=json['name'],
            parent_id=json['parent_id'],
            id=json['id'],
            limits=DepartmentLimits.new(json['limits']),
        )


class DepartmentListResponse:
    items: List[DepartmentItemResponse]
    limit: int
    total_amount: int
    offset: int

    def __init__(
        self,
        items: List[DepartmentItemResponse],
        limit: int,
        total_amount: int,
        offset: int,
    ):
        self.items = items
        self.limit = limit
        self.total_amount = total_amount
        self.offset = offset

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [department.serialize() for department in self.items],
            'limit': self.limit,
            'total_amount': self.total_amount,
            'offset': self.offset,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[DepartmentItemResponse.new(department) for department in json['items']],
            limit=json['limit'],
            total_amount=json['total_amount'],
            offset=json['offset'],
        )


class DepartmentUpdateRequest:
    name: Optional[str] = None
    parent_id: Optional[str] = None

    def __init__(
        self,
        name: Optional[str] = None,
        parent_id: Optional[str] = None,
    ):
        self.name = name
        self.parent_id = parent_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.name is not None:
            data['name'] = self.name
        if self.parent_id is not None:
            data['parent_id'] = self.parent_id
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(name=json.get('name'), parent_id=json.get('parent_id'))


class DepartmentUpdateResponse:
    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        return data

    @classmethod
    def new(cls):
        return cls()


class DepartmentDeleteResponse:
    deleted_ids: List[str]

    def __init__(self, deleted_ids: List[str]):
        self.deleted_ids = deleted_ids

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'deleted_ids': self.deleted_ids}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(deleted_ids=json['deleted_ids'])


class RoutePointExtraData:
    floor: Optional[str] = None
    apartment: Optional[str] = None
    comment: Optional[str] = None
    contact_phone: Optional[str] = None

    def __init__(
        self,
        floor: Optional[str] = None,
        apartment: Optional[str] = None,
        comment: Optional[str] = None,
        contact_phone: Optional[str] = None,
    ):
        self.floor = floor
        self.apartment = apartment
        self.comment = comment
        self.contact_phone = contact_phone

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.floor is not None:
            data['floor'] = self.floor
        if self.apartment is not None:
            data['apartment'] = self.apartment
        if self.comment is not None:
            data['comment'] = self.comment
        if self.contact_phone is not None:
            data['contact_phone'] = self.contact_phone
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            floor=json.get('limit'),
            apartment=json.get('apartment'),
            comment=json.get('comment'),
            contact_phone=json.get('contact_phone'),
        )


class BaseRoutePoint:
    fullname: Optional[str] = None
    geopoint: Optional[List[Union[int, float, Decimal]]] = None
    porchnumber: Optional[str] = None
    extra_data: Optional[RoutePointExtraData] = None

    def __init__(
        self,
        fullname: Optional[str] = None,
        geopoint: Optional[List[Union[int, float, Decimal]]] = None,
        porchnumber: Optional[str] = None,
        extra_data: Optional[RoutePointExtraData] = None,
    ):
        self.fullname = fullname
        self.geopoint = geopoint
        self.porchnumber = porchnumber
        self.extra_data = extra_data

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.fullname is not None:
            data['fullname'] = self.fullname
        if self.geopoint is not None:
            data['geopoint'] = self.geopoint
        if self.porchnumber is not None:
            data['porchnumber'] = self.porchnumber
        if self.extra_data is not None:
            data['extra_data'] = self.extra_data.serialize()

        return data


class RoutePoint(BaseRoutePoint):
    country: Optional[str] = None
    locality: Optional[str] = None
    premisenumber: Optional[str] = None
    thoroughfare: Optional[str] = None

    def __init__(
        self,
        fullname: str,
        geopoint: List[Union[int, float, Decimal]],
        country: Optional[str] = None,
        locality: Optional[str] = None,
        porchnumber: Optional[str] = None,
        premisenumber: Optional[str] = None,
        thoroughfare: Optional[str] = None,
        extra_data: Optional[RoutePointExtraData] = None,
    ):
        super().__init__(
            fullname=fullname,
            geopoint=geopoint,
            porchnumber=porchnumber,
            extra_data=extra_data,
        )
        self.country = country
        self.locality = locality
        self.premisenumber = premisenumber
        self.thoroughfare = thoroughfare

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}

        if self.country is not None:
            data['country'] = self.country
        if self.locality is not None:
            data['locality'] = self.locality
        if self.premisenumber is not None:
            data['premisenumber'] = self.premisenumber
        if self.thoroughfare is not None:
            data['thoroughfare'] = self.thoroughfare

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        extra_data = None
        if 'extra_data' in json:
            extra_data = RoutePointExtraData.new(json['extra_data'])
        return cls(
            fullname=json['fullname'],
            geopoint=json['geopoint'],
            country=json.get('country'),
            locality=json.get('locality'),
            porchnumber=json.get('porchnumber'),
            premisenumber=json.get('premisenumber'),
            thoroughfare=json.get('thoroughfare'),
            extra_data=extra_data,
        )


class RoutePointResponse(BaseRoutePoint):
    passed: Optional[bool] = None

    def __init__(
        self,
        fullname: Optional[str] = None,
        geopoint: Optional[List[Union[int, float, Decimal]]] = None,
        passed: Optional[bool] = None,
        porchnumber: Optional[str] = None,
        extra_data: Optional[RoutePointExtraData] = None,
    ):
        super().__init__(fullname=fullname, geopoint=geopoint, porchnumber=porchnumber, extra_data=extra_data)
        self.passed = passed

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.passed is not None:
            data['passed'] = self.passed

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):

        return cls(
            geopoint=json.get('geopoint'),
            fullname=json.get('fullname'),
            passed=json.get('passed'),
            porchnumber=json.get('porchnumber'),
            extra_data=json.get('extra_data'),
        )


class Order:
    user_id: str
    route: List[RoutePoint]
    class_tariff: str
    due_date: Optional[str] = None
    offer: Optional[str] = None
    requirements: Optional[Dict[str, Union[bool, int, str]]] = None
    cost_center_values: Optional[List[CostCenter]] = None
    comment: Optional[str] = None

    def __init__(
        self,
        user_id: str,
        route: List[RoutePoint],
        class_tariff: str,
        due_date: Optional[str] = None,
        offer: Optional[str] = None,
        requirements: Optional[Dict[str, Union[bool, int, str]]] = None,
        cost_center_values: Optional[List[CostCenter]] = None,
        comment: Optional[str] = None,
    ):
        self.user_id = user_id
        self.class_tariff = class_tariff
        self.route = route
        self.offer = offer
        self.requirements = requirements
        self.cost_center_values = cost_center_values
        self.due_date = due_date
        self.comment = comment

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'user_id': self.user_id,
            'class': self.class_tariff,
            'route': [point.serialize() for point in self.route],
        }

        if self.offer is not None:
            data['offer'] = self.offer
        if self.requirements is not None:
            data['requirements'] = self.requirements
        if self.cost_center_values is not None:
            data['cost_center_values'] = [cost_center.serialize() for cost_center in self.cost_center_values]
        if self.due_date is not None:
            data['due_date'] = self.due_date
        if self.comment is not None:
            data['comment'] = self.comment

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        cost_center_values = None
        if 'cost_center_values' in json:
            cost_center_values = [CostCenter.new(cost_center) for cost_center in json['cost_center_values']]
        return cls(
            user_id=json['user_id'],
            route=[RoutePoint.new(point) for point in json['route']],
            class_tariff=json['class'],
            cost_center_values=cost_center_values,
            due_date=json.get('due_date'),
            offer=json.get('offer'),
            requirements=json.get('requirements'),
            comment=json.get('comment'),
        )


class TaxiOrderItemResponse:
    id: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    class_tariff: Optional[str] = None
    source: Optional[RoutePointResponse] = None
    interim_destinations: Optional[List[RoutePointResponse]] = None
    destination: Optional[RoutePointResponse] = None
    cost_center_values: Optional[List[CostCenter]] = None
    due_date: Optional[str] = None
    finished_date: Optional[str] = None
    cost: Optional[Union[int, float, Decimal]] = None
    cost_with_vat: Optional[Union[int, float, Decimal]] = None

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        class_tariff: Optional[str] = None,
        source: Optional[RoutePointResponse] = None,
        interim_destinations: Optional[List[RoutePointResponse]] = None,
        destination: Optional[RoutePointResponse] = None,
        cost_center_values: Optional[List[CostCenter]] = None,
        due_date: Optional[str] = None,
        finished_date: Optional[str] = None,
        cost: Optional[Union[int, float, Decimal]] = None,
        cost_with_vat: Optional[Union[int, float, Decimal]] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.class_tariff = class_tariff
        self.source = source
        self.interim_destinations = interim_destinations
        self.destination = destination
        self.cost_center_values = cost_center_values
        self.due_date = due_date
        self.finished_date = finished_date
        self.cost = cost
        self.cost_with_vat = cost_with_vat

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.id is not None:
            data['id'] = self.id
        if self.user_id is not None:
            data['user_id'] = self.user_id
        if self.status is not None:
            data['status'] = self.status
        if self.class_tariff is not None:
            data['class'] = self.class_tariff
        if self.source is not None:
            data['source'] = self.source.serialize()
        if self.interim_destinations is not None:
            data['interim_destinations'] = [point.serialize() for point in self.interim_destinations]
        if self.destination is not None:
            data['destination'] = self.destination.serialize()
        if self.cost_center_values is not None:
            data['cost_center_values'] = [cost_center.serialize() for cost_center in self.cost_center_values]
        if self.due_date is not None:
            data['due_date'] = self.due_date
        if self.finished_date is not None:
            data['finished_date'] = self.finished_date
        if self.cost is not None:
            data['cost'] = self.cost
        if self.cost_with_vat is not None:
            data['cost_with_vat'] = self.cost_with_vat
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        source = None
        interim_destinations = None
        destination = None
        cost_center_values = None
        if 'source' in json:
            source = RoutePointResponse.new(json['source'])
        if 'interim_destinations' in json:
            interim_destinations = [RoutePointResponse.new(point) for point in json['interim_destinations']]
        if 'destination' in json:
            destination = RoutePointResponse.new(json['destination'])
        if 'cost_center_values' in json:
            cost_center_values = [CostCenter.new(cost_center) for cost_center in json['cost_center_values']]
        return cls(
            id=json.get('id'),
            user_id=json.get('user_id'),
            status=json.get('status'),
            class_tariff=json.get('class'),
            source=source,
            interim_destinations=interim_destinations,
            destination=destination,
            cost_center_values=cost_center_values,
            due_date=json.get('due_date'),
            finished_date=json.get('finished_date'),
            cost=json.get('cost'),
            cost_with_vat=json.get('cost_with_vat'),
        )


class TaxiOrderListResponse:
    items: List[TaxiOrderItemResponse]
    limit: int
    offset: int
    total_amount: int

    def __init__(
        self,
        items: List[TaxiOrderItemResponse],
        limit: int,
        offset: int,
        total_amount: int,
    ):
        self.items = items
        self.limit = limit
        self.offset = offset
        self.total_amount = total_amount

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'items': [order.serialize() for order in self.items],
            'limit': self.limit,
            'offset': self.offset,
            'total_amount': self.total_amount,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            items=[TaxiOrderItemResponse.new(order) for order in json['items']],
            limit=json['limit'],
            offset=json['offset'],
            total_amount=json['total_amount'],
        )


class TaxiOrderCancelRules:
    can_cancel: Optional[bool] = None
    message: Optional[str] = None
    state: Optional[TaxiOrderCancelRulesState] = None
    title: Optional[str] = None

    def __init__(
        self,
        can_cancel: Optional[bool] = None,
        message: Optional[str] = None,
        state: Optional[TaxiOrderCancelRulesState] = None,
        title: Optional[str] = None,
    ):
        self.can_cancel = can_cancel
        self.message = message
        self.state = state
        self.title = title

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.can_cancel is not None:
            data['can_cancel'] = self.can_cancel
        if self.message is not None:
            data['message'] = self.message
        if self.state is not None:
            data['state'] = self.state.value
        if self.title is not None:
            data['title'] = self.title

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        state = None
        if 'state' in json:
            state = TaxiOrderCancelRulesState(json['state'])
        return cls(
            can_cancel=json.get('can_cancel'),
            message=json.get('message'),
            state=state,
            title=json.get('title'),
        )


class TaxiOrderPerformerVehicle:
    model: Optional[str] = None
    number: Optional[str] = None
    color: Optional[str] = None

    def __init__(
        self,
        model: Optional[str] = None,
        number: Optional[str] = None,
        color: Optional[str] = None,
    ):
        self.model = model
        self.number = number
        self.color = color

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.model is not None:
            data['model'] = self.model
        if self.number is not None:
            data['number'] = self.number
        if self.color is not None:
            data['color'] = self.color

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            model=json.get('model'),
            number=json.get('number'),
            color=json.get('color'),
        )


class TaxiOrderPerformer:
    vehicle: Optional[TaxiOrderPerformerVehicle] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None

    def __init__(
        self,
        vehicle: Optional[TaxiOrderPerformerVehicle] = None,
        fullname: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        self.vehicle = vehicle
        self.fullname = fullname
        self.phone = phone

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.vehicle is not None:
            data['vehicle'] = self.vehicle.serialize()
        if self.fullname is not None:
            data['fullname'] = self.fullname
        if self.phone is not None:
            data['phone'] = self.phone

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        vehicle = None
        if 'vehicle' in json:
            vehicle = TaxiOrderPerformerVehicle.new(json['vehicle'])
        return cls(
            vehicle=vehicle,
            fullname=json.get('fullname'),
            phone=json.get('phone'),
        )


class TaxiOrderGetResponse(TaxiOrderItemResponse):
    performer: Optional[TaxiOrderPerformer] = None
    cancel_rules: Optional[TaxiOrderCancelRules] = None

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        class_tariff: Optional[str] = None,
        source: Optional[RoutePointResponse] = None,
        interim_destinations: Optional[List[RoutePointResponse]] = None,
        destination: Optional[RoutePointResponse] = None,
        cost_center_values: Optional[List[CostCenter]] = None,
        due_date: Optional[str] = None,
        finished_date: Optional[str] = None,
        cost: Optional[Union[int, float, Decimal]] = None,
        cost_with_vat: Optional[Union[int, float, Decimal]] = None,
        performer: Optional[TaxiOrderPerformer] = None,
        cancel_rules: Optional[TaxiOrderCancelRules] = None,
    ):
        super().__init__(
            id,
            user_id,
            status,
            class_tariff,
            source,
            interim_destinations,
            destination,
            cost_center_values,
            due_date,
            finished_date,
            cost,
            cost_with_vat,
        )
        self.performer = performer
        self.cancel_rules = cancel_rules

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {**super().serialize()}
        if self.performer is not None:
            data['performer'] = self.performer.serialize()
        if self.cancel_rules is not None:
            data['cancel_rules'] = self.cancel_rules.serialize()

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        source = None
        interim_destinations = None
        destination = None
        cost_center_values = None
        performer = None
        cancel_rules = None
        if 'source' in json:
            source = RoutePointResponse.new(json['source'])
        if 'interim_destinations' in json:
            interim_destinations = [
                RoutePointResponse.new(interim_destination) for interim_destination in json['interim_destinations']
            ]
        if 'destination' in json:
            destination = RoutePointResponse.new(json['destination'])
        if 'cost_center_values' in json:
            cost_center_values = [CostCenter.new(cost_center) for cost_center in json['cost_center_values']]
        if 'performer' in json:
            performer = TaxiOrderPerformer.new(json['performer'])
        if 'cancel_rules' in json:
            cancel_rules = TaxiOrderCancelRules.new(json['cancel_rules'])
        return cls(
            id=json.get('id'),
            user_id=json.get('user_id'),
            status=json.get('status'),
            class_tariff=json.get('class'),
            source=source,
            interim_destinations=interim_destinations,
            destination=destination,
            cost_center_values=cost_center_values,
            due_date=json.get('due_date'),
            finished_date=json.get('finished_date'),
            cost=json.get('cost'),
            cost_with_vat=json.get('cost_with_vat'),
            performer=performer,
            cancel_rules=cancel_rules,
        )


class TaxiOrderCancelResponse:
    status: TaxiOrderCancelStatus

    def __init__(self, status: TaxiOrderCancelStatus):
        self.status = status

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'status': self.status.value}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(status=TaxiOrderCancelStatus(json['status']))


class OrderCreateResponse:
    order_id: str

    def __init__(self, order_id: str):
        self.order_id = order_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'order_id': self.order_id}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(order_id=json['order_id'])


class TaxiActiveOrderStatus(enum.Enum):
    search: str = 'search'
    driving: str = 'driving'
    waiting: str = 'waiting'
    transporting: str = 'transporting'
    complete: str = 'complete'
    cancelled: str = 'cancelled'
    failed: str = 'failed'
    expired: str = 'expired'
    scheduling: str = 'scheduling'
    scheduled: str = 'scheduled'


class TaxiActiveOrderItemResponse:
    id: str
    status: TaxiActiveOrderStatus

    def __init__(self, id: str, status: TaxiActiveOrderStatus):
        self.id = id
        self.status = status

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'id': self.id,
            'status': self.status.value,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            id=json['id'],
            status=TaxiActiveOrderStatus(json['status']),
        )


class TaxiActiveOrderListResponse:
    items: List[TaxiActiveOrderItemResponse]

    def __init__(self, items: List[TaxiActiveOrderItemResponse]):
        self.items = items

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'items': [item.serialize() for item in self.items]}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(items=[TaxiActiveOrderItemResponse.new(item) for item in json['items']])


class OrderRequest:
    route: List[List[Union[int, float, Decimal]]]
    due: Optional[str] = None
    requirements: Optional[Dict[str, Union[bool, int, str]]] = None
    user_id: Optional[str] = None
    use_toll_roads: Optional[bool] = None

    def __init__(
        self,
        route: List[List[Union[int, float, Decimal]]],
        due: Optional[str] = None,
        requirements: Optional[Dict[str, Union[bool, int, str]]] = None,
        user_id: Optional[str] = None,
        use_toll_roads: Optional[bool] = None,
    ):
        self.route = route
        self.due = due
        self.requirements = requirements
        self.user_id = user_id
        self.use_toll_roads = use_toll_roads

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'route': self.route,
        }

        if self.due is not None:
            data['due'] = self.due
        if self.requirements is not None:
            data['requirements'] = self.requirements
        if self.user_id is not None:
            data['user_id'] = self.user_id
        if self.use_toll_roads is not None:
            data['use_toll_roads'] = self.use_toll_roads

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            due=json.get('due'),
            requirements=json.get('requirements'),
            user_id=json.get('user_id'),
            use_toll_roads=json.get('use_toll_roads'),
            route=json['route'],
        )


class TaxiOrderEstimatedWaiting:
    seconds: int
    message: str

    def __init__(self, seconds: int, message: str):
        self.seconds = seconds
        self.message = message

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'seconds': self.seconds,
            'message': self.message,
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            seconds=json['seconds'],
            message=json['message'],
        )


class TaxiOrderDetailsTariffItem:
    type_tariff: TaxiOrderDetailsTariffItemType
    value: str
    type_details: Optional[str] = None

    def __init__(
        self,
        type_tariff: TaxiOrderDetailsTariffItemType,
        value: str,
        type_details: Optional[str] = None,
    ):
        self.type_tariff = type_tariff
        self.value = value
        self.type_details = type_details

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'type': self.type_tariff.value,
            'value': self.value,
        }

        if self.type_details is not None:
            data['type_details'] = self.type_details

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            type_tariff=TaxiOrderDetailsTariffItemType(json['type']),
            value=json['value'],
            type_details=json.get('type_details'),
        )


class TaxiOrderServiceLevel:
    class_tariff: Optional[str] = None
    is_fixed_price: Optional[bool] = None
    price: Optional[str] = None
    estimated_waiting: Optional[TaxiOrderEstimatedWaiting] = None
    details_tariff: Optional[List[TaxiOrderDetailsTariffItem]] = None

    def __init__(
        self,
        class_tariff: Optional[str] = None,
        is_fixed_price: Optional[bool] = None,
        price: Optional[str] = None,
        estimated_waiting: Optional[TaxiOrderEstimatedWaiting] = None,
        details_tariff: Optional[List[TaxiOrderDetailsTariffItem]] = None,
    ):
        self.class_tariff = class_tariff
        self.is_fixed_price = is_fixed_price
        self.price = price
        self.estimated_waiting = estimated_waiting
        self.details_tariff = details_tariff

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.class_tariff is not None:
            data['class'] = self.class_tariff
        if self.is_fixed_price is not None:
            data['is_fixed_price'] = self.is_fixed_price
        if self.price is not None:
            data['price'] = self.price
        if self.estimated_waiting is not None:
            data['estimated_waiting'] = self.estimated_waiting.serialize()
        if self.details_tariff is not None:
            data['details_tariff'] = [detail.serialize() for detail in self.details_tariff]

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        estimated_waiting = None
        details_tariff = None
        if 'estimated_waiting' in json:
            estimated_waiting = TaxiOrderEstimatedWaiting.new(json['estimated_waiting'])
        if 'details_tariff' in json:
            details_tariff = [TaxiOrderDetailsTariffItem.new(detail) for detail in json['details_tariff']]
        return cls(
            class_tariff=json.get('class'),
            is_fixed_price=json.get('is_fixed_price'),
            price=json.get('price'),
            estimated_waiting=estimated_waiting,
            details_tariff=details_tariff,
        )


class TaxiOrderTollRoads:
    has_tolls: bool
    auto_payment: bool
    price: Optional[str] = None

    def __init__(self, has_tolls: bool, auto_payment: bool, price: Optional[str] = None):
        self.has_tolls = has_tolls
        self.auto_payment = auto_payment
        self.price = price

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'has_tolls': self.has_tolls,
            'auto_payment': self.auto_payment,
        }

        if self.price is not None:
            data['price'] = self.price

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            has_tolls=json['has_tolls'],
            auto_payment=json['auto_payment'],
            price=json.get('price'),
        )


class TaxiOrderRoutestatsGetResponse:
    offer: Optional[str] = None
    service_levels: Optional[List[TaxiOrderServiceLevel]] = None
    toll_roads: Optional[TaxiOrderTollRoads] = None

    def __init__(
        self,
        offer: Optional[str] = None,
        service_levels: Optional[List[TaxiOrderServiceLevel]] = None,
        toll_roads: Optional[TaxiOrderTollRoads] = None,
    ):
        self.offer = offer
        self.service_levels = service_levels
        self.toll_roads = toll_roads

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        if self.offer is not None:
            data['offer'] = self.offer
        if self.service_levels is not None:
            data['service_levels'] = [level.serialize() for level in self.service_levels]
        if self.toll_roads is not None:
            data['toll_roads'] = self.toll_roads.serialize()

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        service_levels = None
        toll_roads = None

        if 'service_levels' in json:
            service_levels = [TaxiOrderServiceLevel.new(level) for level in json['service_levels']]
        if 'toll_roads' in json:
            toll_roads = TaxiOrderTollRoads.new(json['toll_roads'])
        return cls(
            offer=json.get('offer'),
            service_levels=service_levels,
            toll_roads=toll_roads,
        )


class Feedback:
    rating: int
    msg: Optional[str] = None

    def __init__(self, rating: int, msg: Optional[str] = None):
        self.rating = rating
        self.msg = msg

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'rating': self.rating}

        if self.msg is not None:
            data['msg'] = self.msg

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            rating=json['rating'],
            msg=json.get('msg'),
        )


class TaxiFeedbackCreateResponse:
    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        return data

    @classmethod
    def new(cls):
        return cls()


class TaxiOrderDestinationsUpdateRequest:
    created_time: str
    destinations: List[RoutePoint]

    def __init__(self, created_time: str, destinations: List[RoutePoint]):
        self.created_time = created_time
        self.destinations = destinations

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'created_time': self.created_time,
            'destinations': [point.serialize() for point in self.destinations],
        }

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(
            created_time=json['created_time'],
            destinations=[RoutePoint.new(point) for point in json['destinations']],
        )


class TaxiOrderDestinationsUpdateResponse:
    changed_destinations: Optional[List[RoutePoint]] = None

    def __init__(self, changed_destinations: Optional[List[RoutePoint]] = None):
        self.changed_destinations = changed_destinations

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.changed_destinations is not None:
            data['changed_destinations'] = [point.serialize() for point in self.changed_destinations]
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        changed_destinations = None
        if 'changed_destinations' in json:
            changed_destinations = [RoutePoint.new(route) for route in json['changed_destinations']]
        return cls(changed_destinations=changed_destinations)


class VehicleInfo:
    location: List[Union[int, float, Decimal]]

    def __init__(self, location: List[Union[int, float, Decimal]]):
        self.location = location

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'location': self.location}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(location=json['location'])


class TaxiOrderStatusGetResponse:
    status: str
    vehicle: Optional[VehicleInfo] = None
    time_left_raw: Optional[Union[int, float, Decimal]] = None

    def __init__(
        self,
        status: str,
        vehicle: Optional[VehicleInfo] = None,
        time_left_raw: Optional[Union[int, float, Decimal]] = None,
    ):
        self.status = status
        self.vehicle = vehicle
        self.time_left_raw = time_left_raw

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'status': self.status}

        if self.vehicle is not None:
            data['vehicle'] = self.vehicle.serialize()
        if self.time_left_raw is not None:
            data['time_left_raw'] = self.time_left_raw

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        vehicle = None
        if 'vehicle' in json:
            vehicle = VehicleInfo.new(json['vehicle'])
        return cls(
            status=json['status'],
            vehicle=vehicle,
            time_left_raw=json.get('time_left_raw'),
        )


class OrdersCancelRequest:
    state: TaxiOrderCancelRulesState

    def __init__(self, state: TaxiOrderCancelRulesState):
        self.state = state

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'state': self.state.value}

        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(state=TaxiOrderCancelRulesState(json['state']))
