#!/usr/bin/env python3
"""Upload Apollo searches to Notion page."""

import json
import httpx
from pathlib import Path

# Load API key
api_key = Path.home().joinpath(".config/notion/api_key").read_text().strip()
page_id = "2f4de1d9-5312-81c4-bea2-ded1f98898ca"
base_url = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

client = httpx.Client(timeout=30.0, headers=headers)

def add_blocks(blocks):
    response = client.patch(f"{base_url}/blocks/{page_id}/children", json={"children": blocks})
    response.raise_for_status()
    return response.json()

# Data for each persona
personas = [
    {
        "code": "MV-PP-US",
        "name": "Private Practices (General)",
        "target": "Private practice owners, clinic managers (10-50 employees) | Revenue: $500K-$20M | Geography: US",
        "include": "medical practice, private practice, family medicine, primary care, internal medicine, physician practice, doctor office, medical clinic, healthcare practice, outpatient clinic, ambulatory care, patient care, medical group, physician group, clinical practice, general practice, preventive care, wellness clinic, medical office, health clinic, family practice, adult medicine, geriatric care, pediatric care, urgent care, walk-in clinic, community health, rural health, medical center, health center, patient services, clinical services, medical services, healthcare services, physician services, diagnostic services, preventive medicine, chronic care, disease management, care management, population health, value-based care, patient-centered, medical home, PCMH, accountable care, direct primary care, concierge medicine, integrative medicine, holistic health, functional medicine, lifestyle medicine, occupational health, employee health, corporate health, executive health, travel medicine, sports medicine, womens health, mens health, senior care, elder care, adolescent medicine, preventive screening, health screening, annual wellness, physical exam, chronic disease, diabetes care, hypertension, cardiovascular, respiratory care, weight management, nutrition counseling, health coaching, care coordination, referral management, clinical operations, practice management, medical billing, revenue cycle, EHR, EMR, electronic health, health records, patient portal, telehealth, telemedicine, virtual care, remote patient, RPM, healthcare technology, practice technology, medical scheduling, appointment scheduling, patient scheduling, front office, back office, clinical staff, medical staff, physician employment, healthcare staffing, medical recruiting, credentialing, compliance, HIPAA, quality metrics, MIPS, MACRA, Medicare, Medicaid, commercial payer, insurance verification, prior authorization, claims management, denial management, patient collections, patient billing, statement processing, payment processing, patient engagement, patient communication, patient retention, patient satisfaction, patient experience, clinical workflow, operational efficiency, practice growth, practice expansion, multi-location, group practice, solo practice, independent practice, physician-owned",
        "exclude": "hospital, health system, university, academic, research institute, pharmaceutical, biotech, medical device, insurance company, payer, health plan, staffing agency, recruiting firm, consulting firm, software vendor, IT company, laboratory, imaging center, dialysis, hospice, home health, skilled nursing, nursing home, long-term care, rehabilitation center, mental health facility, substance abuse, addiction treatment, veterinary, animal hospital, government, federal, state agency, military, VA hospital, correctional",
        "roles": "Practice Owner, Managing Partner, Practice Administrator, Practice Manager, Office Manager, Clinical Director, Medical Director, Chief Medical Officer, Chief Operating Officer, Chief Executive Officer, Physician Owner, Partner Physician, Managing Physician, Director of Operations, Director of Clinical Operations, Business Manager, Healthcare Administrator, Clinic Manager, Clinic Director, Operations Manager, Executive Director"
    },
    {
        "code": "MV-DEN-US",
        "name": "Dental Practices",
        "target": "Dentist owners, dental practice managers (10-50 employees) | Revenue: $500K-$20M | Geography: US",
        "include": "dental practice, dentist office, dental clinic, dental group, dental care, oral health, family dentistry, general dentistry, cosmetic dentistry, restorative dentistry, preventive dentistry, pediatric dentistry, orthodontics, orthodontist, braces, Invisalign, clear aligners, periodontics, periodontist, gum disease, periodontal, endodontics, endodontist, root canal, oral surgery, oral surgeon, wisdom teeth, dental implants, implant dentistry, prosthodontics, prosthodontist, dentures, dental crowns, dental bridges, veneers, teeth whitening, dental hygiene, dental cleaning, dental exam, dental x-ray, dental imaging, digital dentistry, CAD CAM, CEREC, 3D printing, dental lab, dental laboratory, dental technology, dental equipment, dental supplies, dental materials, dental software, dental practice management, dental billing, dental insurance, dental claims, dental scheduling, dental front office, dental receptionist, dental assistant, dental hygienist, dental staff, dental team, dental training, dental continuing education, dental marketing, dental website, dental SEO, dental social media, patient acquisition, new patient, patient retention, patient referral, dental membership, dental savings plan, dental financing, CareCredit, dental PPO, dental HMO, fee-for-service, dental revenue, dental production, dental collections, dental profitability, dental growth, dental expansion, multi-location dental, dental DSO, dental support organization, dental partnership, dental associate, dental recruitment, dental HR, dental compliance, OSHA dental, dental infection control, dental sterilization, dental safety, dental quality, patient experience, patient satisfaction, dental reviews, dental reputation, dental office design, dental construction, dental real estate, dental lease, dental startup, dental acquisition, dental valuation, dental transition, dental retirement, dental consulting, dental coaching, dental leadership, dental management, dental operations, dental efficiency, dental productivity, dental KPI, dental metrics, dental analytics, dental reporting, smile design, smile makeover, full mouth, dental emergency, same-day dentistry, sedation dentistry, sleep dentistry, dental anxiety, dental phobia, TMJ, TMD, dental sleep medicine, sleep apnea, oral appliance, night guard, sports guard, dental wellness, holistic dentistry, biological dentistry, mercury-free, metal-free",
        "exclude": "dental school, dental university, dental college, dental research, dental manufacturer, dental distributor, dental supplier, dental equipment company, dental software company, dental insurance company, dental staffing, dental temp agency, dental consulting firm, dental DSO corporate, private equity dental, hospital dentistry, VA dental, military dental, correctional dental, community health center, FQHC, mobile dental, dental charity, nonprofit dental, dental mission, veterinary dental, animal dental, dental laboratory only, denture lab",
        "roles": "Dentist Owner, Practice Owner, Managing Partner, Dental Practice Administrator, Practice Manager, Office Manager, Dental Director, Clinical Director, Chief Dental Officer, Chief Executive Officer, Chief Operating Officer, Partner Dentist, Managing Dentist, Lead Dentist, Associate Dentist, Orthodontist Owner, Periodontist Owner, Oral Surgeon Owner, Endodontist Owner, Director of Operations, Business Manager, Regional Manager, Multi-Location Manager, Dental Operations Manager"
    },
    {
        "code": "MV-CHI-US",
        "name": "Chiropractic Practices",
        "target": "Chiropractor owners, clinic directors (3-25 employees) | Revenue: $500K-$20M | Geography: US",
        "include": "chiropractic, chiropractor, chiropractic clinic, chiropractic practice, chiropractic care, chiropractic office, spinal adjustment, spinal manipulation, spinal decompression, spine care, spine clinic, back pain, neck pain, joint pain, musculoskeletal, MSK, neuromusculoskeletal, subluxation, vertebral, cervical, thoracic, lumbar, sacral, pelvic, posture correction, postural, alignment, biomechanics, kinesiology, functional movement, movement assessment, gait analysis, ergonomics, workplace wellness, corporate wellness, wellness center, wellness clinic, holistic health, integrative health, natural health, alternative medicine, complementary medicine, drug-free, non-surgical, conservative care, manual therapy, soft tissue, myofascial, trigger point, active release, ART, Graston, IASTM, dry needling, acupuncture, cupping, massage therapy, therapeutic massage, rehabilitation, rehab, physical therapy, physiotherapy, exercise therapy, corrective exercise, therapeutic exercise, strengthening, stretching, flexibility, mobility, range of motion, sports chiropractic, sports medicine, sports injury, athletic performance, athlete care, sports rehab, injury prevention, injury recovery, pain management, pain relief, chronic pain, acute pain, sciatica, herniated disc, disc injury, whiplash, auto injury, car accident, personal injury, workers comp, work injury, slip and fall, headache, migraine, neuropathy, radiculopathy, carpal tunnel, shoulder pain, knee pain, hip pain, extremity, upper extremity, lower extremity, pediatric chiropractic, prenatal chiropractic, pregnancy, Webster technique, family chiropractic, geriatric chiropractic, senior care, nutritional counseling, lifestyle coaching, weight loss, detox, functional nutrition, supplement, vitamin, health optimization, peak performance, biohacking, nervous system, neurological, brain health, cognitive, x-ray, imaging, diagnostic, assessment, examination, treatment plan, care plan, maintenance care, wellness care, patient education, community education, health workshop, screening event, chiropractic EHR, practice management, chiropractic billing, insurance billing, cash practice, membership model, chiropractic marketing, patient acquisition, patient retention, referral, chiropractic growth, multi-location, chiropractic franchise",
        "exclude": "chiropractic school, chiropractic college, chiropractic university, chiropractic research, chiropractic association, chiropractic board, chiropractic supplier, chiropractic equipment, chiropractic software company, chiropractic consulting, franchise corporate, hospital, health system, orthopedic surgery, neurosurgery, pain clinic, interventional pain, physical therapy chain, PT corporate, staffing agency, recruiting firm, insurance company, workers comp carrier, personal injury attorney, law firm, veterinary chiropractic, animal chiropractic, equine",
        "roles": "Chiropractor Owner, Practice Owner, Clinic Owner, Managing Partner, Chiropractic Director, Clinical Director, Chief Executive Officer, Chief Operating Officer, Practice Administrator, Practice Manager, Office Manager, Clinic Manager, Director of Operations, Business Manager, Lead Chiropractor, Associate Chiropractor, Partner Chiropractor, Rehabilitation Director, Wellness Director, Multi-Location Director, Regional Manager"
    },
    {
        "code": "MV-AES-US",
        "name": "Aesthetics / MedSpa",
        "target": "MedSpa owners, cosmetic practice owners (5-30 employees) | Revenue: $500K-$20M | Geography: US",
        "include": "medical spa, medspa, med spa, aesthetic clinic, aesthetics practice, cosmetic clinic, cosmetic practice, beauty clinic, anti-aging clinic, rejuvenation center, skin clinic, skincare clinic, dermatology practice, cosmetic dermatology, aesthetic dermatology, plastic surgery, cosmetic surgery, facial plastic surgery, body contouring, body sculpting, liposuction, tummy tuck, abdominoplasty, breast augmentation, rhinoplasty, facelift, eyelid surgery, blepharoplasty, neck lift, brow lift, injectable, neurotoxin, Botox, Dysport, Xeomin, Jeuveau, dermal filler, hyaluronic acid, Juvederm, Restylane, Sculptra, Radiesse, Kybella, lip filler, cheek filler, jawline, facial balancing, liquid facelift, PDO threads, thread lift, PRP, platelet-rich plasma, vampire facial, microneedling, collagen induction, skin rejuvenation, skin resurfacing, laser treatment, laser clinic, laser aesthetics, IPL, photofacial, BBL, broadband light, fractional laser, CO2 laser, Fraxel, Halo, Clear Brilliant, Morpheus8, RF microneedling, radiofrequency, Thermage, Ultherapy, skin tightening, body tightening, CoolSculpting, cryolipolysis, fat reduction, cellulite, Emtone, Emsculpt, muscle toning, truSculpt, Vanquish, non-invasive, non-surgical, minimally invasive, aesthetic procedure, cosmetic procedure, beauty treatment, facial treatment, skin treatment, chemical peel, microdermabrasion, dermaplaning, HydraFacial, oxygen facial, LED therapy, acne treatment, acne scar, scar treatment, pigmentation, melasma, sun damage, age spots, brown spots, rosacea, vein treatment, spider vein, varicose vein, sclerotherapy, laser vein, hair removal, laser hair removal, electrolysis, hair restoration, PRP hair, weight loss, medical weight loss, semaglutide, Ozempic, Wegovy, tirzepatide, hormone therapy, HRT, bioidentical hormones, testosterone, peptide therapy, IV therapy, vitamin infusion, wellness injection, B12, NAD, glutathione, regenerative aesthetics, stem cell, exosome, aesthetic medicine, cosmetic medicine, beauty industry, aesthetic industry, patient consultation, treatment plan, before after, aesthetic results, patient transformation, luxury aesthetics, boutique medspa, concierge aesthetics, VIP treatment, membership program, aesthetic membership, skincare products, medical grade skincare, retail skincare, ZO Skin Health, SkinCeuticals, Obagi, Alastin, aesthetic marketing, medspa marketing, social media aesthetic, Instagram beauty, influencer, aesthetic training, injector training, aesthetic certification",
        "exclude": "hospital, health system, university, academic medical center, research institute, pharmaceutical company, biotech, medical device manufacturer, aesthetic device manufacturer, laser manufacturer, skincare manufacturer, cosmetic distributor, beauty distributor, aesthetic supplier, spa equipment, staffing agency, recruiting firm, consulting firm, software company, marketing agency, training academy, aesthetic school, beauty school, cosmetology school, esthetician school, day spa, nail salon, hair salon, tanning salon, tattoo, permanent makeup only, franchise corporate, private equity, insurance company",
        "roles": "MedSpa Owner, Practice Owner, Clinic Owner, Medical Director, Aesthetic Director, Clinical Director, Chief Executive Officer, Chief Operating Officer, Chief Medical Officer, Managing Partner, Partner Physician, Cosmetic Surgeon, Plastic Surgeon, Dermatologist Owner, Aesthetic Physician, Practice Administrator, Practice Manager, Spa Director, Spa Manager, Operations Director, Business Manager, Director of Aesthetics, Lead Injector, Nurse Practitioner Owner, PA Owner, Director of Client Services"
    }
]

print("Adding remaining personas to Notion...")

for p in personas[1:]:  # Skip first one since we partially added it
    blocks = [
        {"object": "block", "type": "divider", "divider": {}},
        {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": f"{p['code']} - {p['name']}"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"Target: {p['target']}"}}]}},
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "INCLUDE Keywords"}}]}},
        {"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": p['include']}}], "language": "plain text"}},
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "EXCLUDE Keywords"}}]}},
        {"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": p['exclude']}}], "language": "plain text"}},
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "Target Roles"}}]}},
        {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": p['roles']}}]}}
    ]
    add_blocks(blocks)
    print(f"  Added {p['code']}")

# Add exclude/roles for first persona (we already added include)
pp = personas[0]
blocks = [
    {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "EXCLUDE Keywords"}}]}},
    {"object": "block", "type": "code", "code": {"rich_text": [{"text": {"content": pp['exclude']}}], "language": "plain text"}},
    {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"text": {"content": "Target Roles"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": pp['roles']}}]}}
]

# Need to insert these after the first include block - tricky with Notion API
# For now, add at end with a note
blocks_with_note = [
    {"object": "block", "type": "divider", "divider": {}},
    {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "MV-PP-US Additional Fields"}}]}},
] + blocks

add_blocks(blocks_with_note)
print("  Added MV-PP-US exclude/roles")

print(f"\nDone! View at: https://www.notion.so/MedVirtual-Apollo-Searches-2f4de1d9531281c4bea2ded1f98898ca")
