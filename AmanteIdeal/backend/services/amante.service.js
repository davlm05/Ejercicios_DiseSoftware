import { AmanteRepository } from '../repositories/amante.repository.js';
import { CreateAmanteDTO } from '../dtos/amante.dto.js';

const amanteRepository = new AmanteRepository();

export class AmanteService {
    async createAmante(data) {
        const dto = new CreateAmanteDTO(data);
        const errors = dto.validate();
        
        if (errors.length > 0) {
            throw new Error(`Validation Error: ${errors.join(' ')}`);
        }

        return await amanteRepository.create({
            nombre: dto.nombre,
            edad: dto.edad,
            intereses: dto.intereses
        });
    }

    async getAmantesByInterest(interes) {
        if (!interes) {
            return await amanteRepository.findAll();
        }
        return await amanteRepository.findByInterest(interes);
    }
}
