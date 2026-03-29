import { Router } from 'express';
import { AmanteController } from '../controllers/amante.controller.js';

const router = Router();
const amanteController = new AmanteController();

router.post('/', (req, res) => amanteController.create(req, res));
router.get('/', (req, res) => amanteController.getByInterest(req, res));

export default router;
