import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function PatientHeader() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="font-headline text-secondary-foreground">Patient Details</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col md:flex-row items-start md:items-center gap-6">
        <Avatar className="w-20 h-20">
          <AvatarImage src="https://placehold.co/80x80.png" alt="Patient John Doe" data-ai-hint="patient photography"/>
          <AvatarFallback>JD</AvatarFallback>
        </Avatar>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-x-8 gap-y-4 text-sm w-full">
          <div><span className="font-medium text-muted-foreground">Name:</span><p className="font-semibold">John Doe</p></div>
          <div><span className="font-medium text-muted-foreground">Gender:</span><p className="font-semibold">Male</p></div>
          <div><span className="font-medium text-muted-foreground">Age:</span><p className="font-semibold">45</p></div>
          <div><span className="font-medium text-muted-foreground">NAT ID:</span><p className="font-semibold">123-456-789</p></div>
          <div><span className="font-medium text-muted-foreground">Nationality:</span><p className="font-semibold">American</p></div>
          <div className="col-span-2 md:col-span-1"><span className="font-medium text-muted-foreground">Insurance:</span><p className="font-semibold">Blue Cross Shield</p></div>
        </div>
      </CardContent>
    </Card>
  );
}
