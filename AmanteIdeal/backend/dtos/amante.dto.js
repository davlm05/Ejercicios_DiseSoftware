export class CreateAmanteDTO {
    constructor(data) {
        this.nombre = data.nombre;
        this.edad = Number(data.edad);
        
        // Handle both Array and comma-separated string for intereses
        if (Array.isArray(data.intereses)) {
            this.intereses = data.intereses;
        } else if (typeof data.intereses === 'string') {
            this.intereses = data.intereses.split(',').map(i => i.trim()).filter(i => i !== '');
        } else {
            this.intereses = [];
        }
    }

    validate() {
        const errors = [];
        if (!this.nombre || typeof this.nombre !== 'string') {
            errors.push('El nombre es requerido y debe ser texto.');
        }
        if (!this.edad || typeof this.edad !== 'number' || isNaN(this.edad) || this.edad < 18) {
            errors.push('La edad es requerida, debe ser número y mayor o igual a 18.');
        }
        if (!this.intereses || !Array.isArray(this.intereses) || this.intereses.length === 0) {
            errors.push('Los intereses son requeridos. Mínimo uno.');
        }
        return errors;
    }
}
