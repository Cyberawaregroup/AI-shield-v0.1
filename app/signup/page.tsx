"use client";
import { useState } from "react";
import { Input } from "../../components/ui/input";
import { Button } from "../../components/ui/button";
import Link from "next/link";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);
    try {
      const res = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Signup failed");
      }
      setSuccess(true);
      setUsername("");
      setPassword("");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form
        onSubmit={handleSignup}
        className="bg-white p-8 rounded shadow-md w-full max-w-md space-y-6"
      >
        <h2 className="text-2xl font-bold text-center">Sign Up</h2>
        <Input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Signing up..." : "Sign Up"}
        </Button>
        {error && <div className="text-red-500 text-center">{error}</div>}
        {success && <div className="text-green-600 text-center">Signup successful! You can now log in.</div>}
      </form>
      <div className="mt-4 text-center">
        <span>Already have an account? </span>
        <Link href="/login" className="text-blue-600 hover:underline">Log in</Link>
      </div>
    </div>
  );
} 