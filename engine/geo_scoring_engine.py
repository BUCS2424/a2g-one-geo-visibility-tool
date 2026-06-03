import pandas as pd
import numpy as np

class GEOScoringEngine:
    """
    The 2026 GEO & AEO Audit Engine.
    Calculates brand visibility scores based on 29 structured signals.
    """
    
    def __init__(self):
        # Weighted scoring pillars based on 2026 industry standards
        self.weights = {
            "technical_schema": 25,       # Schema 2.0 & Extractability
            "content_conversational": 20, # Answer-first & rhythm
            "entity_trust": 15,           # E-E-A-T & GBP signals
            "off_site_authority": 30,     # Citations & mentions
            "freshness": 10               # Update velocity
        }

    def calculate_visibility_score(self, site_data):
        """
        Main scoring function. 
        Expects a dictionary of site attributes extracted by crawler.
        """
        scores = {}
        
        # 1. Technical & Schema (Pillar 1 - 25 Pts)
        tech_points = 0
        if site_data.get('has_schema_2_0', False): tech_points += 10
        if site_data.get('has_speakable_schema', False): tech_points += 8
        if site_data.get('mobile_score', 0) > 90: tech_points += 7
        scores['technical_schema'] = tech_points

        # 2. Content Conversationality (Pillar 2 - 20 Pts)
        content_points = 0
        avg_section_length = site_data.get('avg_words_per_section', 0)

        if 120 <= avg_section_length <= 180:
            content_points += 10
        elif 50 <= avg_section_length < 120 or 180 < avg_section_length <= 250:
            content_points += 5
            
        if site_data.get('has_answer_first_blocks', False): content_points += 10
        scores['content_conversational'] = content_points

        # 3. Entity & Trust (Pillar 3 - 15 Pts)
        trust_points = 0
        if site_data.get('nap_consistent', False): trust_points += 5
        if site_data.get('has_verified_author', False): trust_points += 5
        if site_data.get('gbp_rating', 0) >= 4.2: 
            trust_points += 5
        scores['entity_trust'] = trust_points

        # 4. Off-Site Authority (Pillar 4 - 30 Pts)
        authority_points = 0
        if site_data.get('review_velocity_high', False): authority_points += 15
        if site_data.get('top_10_list_mentions', 0) > 0: authority_points += 15
        scores['off_site_authority'] = authority_points

        # 5. Freshness (Pillar 5 - 10 Pts)
        fresh_points = 0
        if site_data.get('days_since_update', 999) <= 90:
            fresh_points += 10
        scores['freshness'] = fresh_points

        # Final Weighted Calculation
        total_score = sum(scores.values())
        return total_score, scores
