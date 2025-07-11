"use client";
import { SidebarMenu, SidebarMenuItem, SidebarMenuButton } from "@/components/ui/sidebar";
import { LayoutDashboard, Users, HeartPulse as PatientIcon, FileText, Settings } from "lucide-react";
import { usePathname } from "next/navigation";

export function SidebarNav() {
  const pathname = usePathname();
  const isActive = (path: string) => pathname === path;

  return (
    <SidebarMenu>
        <SidebarMenuItem>
            <SidebarMenuButton href="#" isActive={isActive('/')} tooltip="Dashboard">
                <LayoutDashboard />
                Dashboard
            </SidebarMenuButton>
        </SidebarMenuItem>
        <SidebarMenuItem>
            <SidebarMenuButton href="#" isActive={isActive('/patients')} tooltip="Patients">
                <PatientIcon />
                Patients
            </SidebarMenuButton>
        </SidebarMenuItem>
        <SidebarMenuItem>
            <SidebarMenuButton href="#" isActive={isActive('/staff')} tooltip="Staff">
                <Users />
                Staff
            </SidebarMenuButton>
        </SidebarMenuItem>
        <SidebarMenuItem>
            <SidebarMenuButton href="#" isActive={isActive('/reports')} tooltip="Reports">
                <FileText />
                Reports
            </SidebarMenuButton>
        </SidebarMenuItem>
        <SidebarMenuItem>
            <SidebarMenuButton href="#" isActive={isActive('/settings')} tooltip="Settings">
                <Settings />
                Settings
            </SidebarMenuButton>
        </SidebarMenuItem>
    </SidebarMenu>
  );
}
