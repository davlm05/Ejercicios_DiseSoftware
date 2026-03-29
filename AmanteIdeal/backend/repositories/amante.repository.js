import { Amante } from '../models/amante.model.js';

export class AmanteRepository {
    async create(data) {
        const nuevoAmante = new Amante(data);
        return await nuevoAmante.save();
    }

    async findByInterest(interes) {
        return await Amante.find({ intereses: { $regex: interes, $options: 'i' } });
    }

    async findAll() {
        return await Amante.find();
    }
}
