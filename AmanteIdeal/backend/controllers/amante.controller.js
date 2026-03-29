import { AmanteService } from '../services/amante.service.js';

const amanteService = new AmanteService();

export class AmanteController {
    async create(req, res) {
        try {
            const amante = await amanteService.createAmante(req.body);
            res.status(201).json({ success: true, data: amante });
        } catch (error) {
            res.status(400).json({ success: false, message: error.message });
        }
    }

    async getByInterest(req, res) {
        try {
            const { interes } = req.query;
            const amantes = await amanteService.getAmantesByInterest(interes);
            res.status(200).json({ success: true, data: amantes });
        } catch (error) {
            res.status(500).json({ success: false, message: 'Server error' });
        }
    }
}
