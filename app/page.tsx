"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import App from "../app";

export default function Page() {
  const [authChecked, setAuthChecked] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
    if (!token) {
      router.replace("/login");
    } else {
      setIsAuthenticated(true);
    }
    setAuthChecked(true);
  }, [router]);

  if (!authChecked) {
    return null; // Or a loading spinner
  }
  if (!isAuthenticated) {
    return null;
  }
  return <App />;
}
