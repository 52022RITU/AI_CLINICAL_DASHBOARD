import { Card, CardContent } from "@/components/ui/card";
import { Thermometer, Activity, HeartPulse, Weight, Ruler } from "lucide-react";

const vitals = [
  { name: "Temperature", value: "37°C", icon: Thermometer },
  { name: "Blood Pressure", value: "120/80", unit: "mmHg", icon: Activity },
  { name: "Heart Rate", value: "72", unit: "bpm", icon: HeartPulse },
  { name: "Weight", value: "85", unit: "kg", icon: Weight },
  { name: "Height", value: "180", unit: "cm", icon: Ruler },
];

export function VitalsBar() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {vitals.map((vital) => (
        <Card key={vital.name}>
          <CardContent className="p-4 flex items-center gap-4">
            <vital.icon className="w-8 h-8 text-primary shrink-0" />
            <div>
              <p className="text-sm text-muted-foreground">{vital.name}</p>
              <p className="text-lg font-bold text-secondary-foreground">
                {vital.value}
                {vital.unit && <span className="text-sm font-normal text-muted-foreground ml-1">{vital.unit}</span>}
              </p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
