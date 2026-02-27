"""
Data models for lunch box orders and related entities.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class BoxType(str, Enum):
    """Standard box types available."""
    VEG_COMFORT = "Veg Comfort Box"
    NON_VEG_COMFORT = "Non-Veg Comfort Box"
    VEG_SPECIAL = "Veg Special Box"
    NON_VEG_SPECIAL = "Non-Veg Special Box"
    KABULI_CHANA = "Kabuli Chana Box"
    MOONG_DAL = "Moong Dal Box"
    RAJMA = "Rajma Box"
    UNKNOWN = "Unknown"


class RiceType(str, Enum):
    """Standard rice types available."""
    PULAV = "Pulav Rice"
    WHITE = "White Rice"
    UNKNOWN = "Unknown"


@dataclass
class Order:
    """Represents a single lunch box order."""
    
    name: str
    address: str
    box_type: str
    rice_type: str
    order_id: Optional[int] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Normalize string fields after initialization."""
        self.name = self.name.strip() if self.name else ""
        self.address = self.address.strip() if self.address else ""
        self.box_type = self.box_type.strip() if self.box_type else ""
        self.rice_type = self.rice_type.strip() if self.rice_type else ""
        
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary."""
        return {
            'name': self.name,
            'address': self.address,
            'box_type': self.box_type,
            'rice_type': self.rice_type,
            'order_id': self.order_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'metadata': self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        """Create order from dictionary."""
        return cls(
            name=data.get('name', ''),
            address=data.get('address', ''),
            box_type=data.get('box_type', ''),
            rice_type=data.get('rice_type', ''),
            order_id=data.get('order_id'),
            timestamp=data.get('timestamp'),
            metadata=data.get('metadata'),
        )


@dataclass
class Summary:
    """Represents a summary report of orders."""
    
    total_boxes: int
    box_combinations: Dict[str, int]
    address_counts: Dict[str, int]
    generated_at: datetime
    date_for: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        return {
            'total_boxes': self.total_boxes,
            'box_combinations': self.box_combinations,
            'address_counts': self.address_counts,
            'generated_at': self.generated_at.isoformat(),
            'date_for': self.date_for,
        }
