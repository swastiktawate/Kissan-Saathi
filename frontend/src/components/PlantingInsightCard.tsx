import { Lightbulb } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import type { PlantingInsight } from '../utils/plantingInsights';

interface Props {
    insight: PlantingInsight | null;
}

export default function PlantingInsightCard({ insight }: Props) {
    const { t } = useLanguage();

    if (!insight || !insight.show) {
        return null;
    }

    return (
        <div className="bg-green-50 border border-green-200 shadow-sm rounded-xl p-4 flex gap-4 items-start relative overflow-hidden animate-fade-in-up mt-4">
            <div className="bg-green-100 text-green-700 p-2 rounded-full shrink-0">
                <Lightbulb size={24} />
            </div>
            
            <div>
                <h3 className="text-sm font-bold text-green-900 uppercase tracking-wide flex items-center gap-2">
                    {t('smart_insight_title')}
                </h3>
                
                <p className="text-gray-700 text-sm mt-1 leading-relaxed">
                    Prices for <strong className="text-green-800">{insight.crop}</strong> are predicted to surge to <strong className="text-green-800">₹{insight.peakPrice}/q</strong> around <strong className="text-green-800">{insight.peakDate}</strong>. Since this crop takes ~{insight.growthDays} days to harvest, you should start planting around <strong className="text-green-800 bg-green-200 px-1 py-0.5 rounded">{insight.optimalPlantingDate}</strong> to maximize your profit.
                </p>
            </div>
        </div>
    );
}
