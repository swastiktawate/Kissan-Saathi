export interface ForecastPoint {
    date: string;
    predicted_price: number;
}

export interface PlantingInsight {
    show: boolean;
    peakDate: string;
    peakPrice: number;
    optimalPlantingDate: string;
    growthDays: number;
    hikePercentage: number;
    crop: string;
}

export function generatePlantingInsight(
    forecastData: ForecastPoint[], 
    crop: string, 
    startDateStr?: string
): PlantingInsight | null {
    if (!forecastData || forecastData.length === 0) return null;

    const GROWTH_CYCLES: Record<string, number> = {
        "Tomato": 90,
        "Onion": 120,
        "Potato": 100,
        "Banana": 300
    };
    
    // Normalize crop key
    const normalizedCrop = Object.keys(GROWTH_CYCLES).find(k => k.toLowerCase() === crop.toLowerCase()) || "Other";
    const growthDays = GROWTH_CYCLES[normalizedCrop] || 90;
    
    const startDate = startDateStr ? new Date(startDateStr) : new Date(forecastData[0].date);
    const startPrice = forecastData[0].predicted_price;
    
    // Valid harvest window starts after 'growthDays' from startDate
    const validHarvestStartDate = new Date(startDate);
    validHarvestStartDate.setDate(validHarvestStartDate.getDate() + growthDays);
    
    let peakPoint = forecastData[0];
    let foundValid = false;
    
    for (const point of forecastData) {
        const pointDate = new Date(point.date);
        if (pointDate >= validHarvestStartDate) {
            if (!foundValid || point.predicted_price > peakPoint.predicted_price) {
                peakPoint = point;
                foundValid = true;
            }
        }
    }
    
    if (!foundValid) return null;
    
    const hikePercentage = ((peakPoint.predicted_price - startPrice) / startPrice) * 100;
    
    // Only suggest if peak is at least 15% higher than today's price
    if (hikePercentage < 15) {
        return { show: false, peakDate: "", peakPrice: 0, optimalPlantingDate: "", growthDays, hikePercentage, crop: normalizedCrop };
    }
    
    const peakDateObj = new Date(peakPoint.date);
    const optimalPlantingDateObj = new Date(peakDateObj);
    optimalPlantingDateObj.setDate(optimalPlantingDateObj.getDate() - growthDays);
    
    // Safety check so we don't recommend planting in the past
    if (optimalPlantingDateObj < startDate) {
        optimalPlantingDateObj.setTime(startDate.getTime());
    }

    const formatDate = (d: Date) => d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

    return {
        show: true,
        peakDate: formatDate(peakDateObj),
        peakPrice: Math.round(peakPoint.predicted_price),
        optimalPlantingDate: formatDate(optimalPlantingDateObj),
        growthDays,
        hikePercentage: Math.round(hikePercentage),
        crop: normalizedCrop
    };
}
