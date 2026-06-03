import express from 'express';
import { authenticate } from '../middleware/auth.js';
import Audit from '../models/Audit.js';

const router = express.Router();

// Create new audit
router.post('/', authenticate, async (req, res) => {
  try {
    const { businessUrl, businessName, businessIndustry } = req.body;
    
    if (!businessUrl) {
      return res.status(400).json({ error: 'Business URL required' });
    }
    
    // TODO: Call Python GEO Engine to analyze the website
    const audit = new Audit({
      userId: req.user.userId,
      businessUrl,
      businessName,
      businessIndustry,
      score: 0,
      breakdown: {},
      details: {},
      recommendations: [],
    });
    
    await audit.save();
    res.status(201).json(audit);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get audit by ID
router.get('/:id', authenticate, async (req, res) => {
  try {
    const audit = await Audit.findById(req.params.id);
    
    if (!audit) {
      return res.status(404).json({ error: 'Audit not found' });
    }
    
    if (audit.userId.toString() !== req.user.userId) {
      return res.status(403).json({ error: 'Unauthorized' });
    }
    
    res.json(audit);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// List user audits
router.get('/', authenticate, async (req, res) => {
  try {
    const audits = await Audit.find({ userId: req.user.userId }).sort({ createdAt: -1 });
    res.json(audits);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update audit
router.patch('/:id', authenticate, async (req, res) => {
  try {
    const audit = await Audit.findById(req.params.id);
    
    if (!audit) {
      return res.status(404).json({ error: 'Audit not found' });
    }
    
    if (audit.userId.toString() !== req.user.userId) {
      return res.status(403).json({ error: 'Unauthorized' });
    }
    
    Object.assign(audit, req.body);
    audit.updatedAt = Date.now();
    await audit.save();
    
    res.json(audit);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
