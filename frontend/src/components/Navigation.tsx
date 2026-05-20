"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Home, Info } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "Home", icon: Home, href: "/" },
  { label: "Info", icon: Info, href: "/settings" },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <div className="fixed bottom-5 left-1/2 -translate-x-1/2 w-[90%] max-w-sm z-50">
      <nav className="bg-[#fffaf2] border border-[#d6e7e8] p-2 rounded-lg shadow-[0_10px_24px_rgba(24,50,63,0.10)] flex justify-center gap-5 items-center">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "relative flex flex-col items-center justify-center w-14 h-14 rounded-lg transition-all duration-200",
                isActive ? "bg-primary text-white shadow-sm" : "text-slate-500 hover:text-primary hover:bg-[#e6f4f1]"
              )}
            >
              <Icon className="w-6 h-6 stroke-[2.2px]" />
              {isActive && (
                <motion.div
                  layoutId="nav-glow"
                  className="absolute -bottom-1 w-1 h-1 bg-[#fffaf2] rounded-full"
                />
              )}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
