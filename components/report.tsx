"use client";
import { z } from "zod";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

import { Dropzone } from "@/components/ui/dropzone";
          // wrapper over react-dropzone
import axios from "axios";
import { toast } from "sonner";                               // shadcn toast
import { Form, FormField, FormItem, FormControl, FormLabel, FormMessage } from "./ui/form";

const scamTypes = [
    "phishing",        // change these to match your actual scam types
    "fake_website",
    "investment",
    "tech_support",
    "romance",
    "job",
    "impersonation",
    "other"
  ] as const;

const paymentMethods = [
    "bank_transfer",
    "credit_card",
    "debit_card",
    "paypal",
    "other"
  ] as const;

const ageGroupOptions = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+"
  ] as const;

// ---- 1.  Zod schema generated from the server model ----
export const reportSchema = z.object({
  reporterName:      z.string().max(255).optional(),
  reporterEmail:     z.string().email().optional(),
  reporterPhone:     z.string().max(50).optional(),
  incidentDate:      z.coerce.date(),
  incidentTime:      z.string().regex(/^([01]?\d|2[0-3]):[0-5]\d$/).optional(),
  scamType:          z.enum(scamTypes),
  otherScamType:     z.string().max(255).optional(),
  description:       z.string().min(10).max(1000),
  howScamBegan:      z.string().max(500).optional(),
  moneyLost:         z.boolean().default(false),
  amountLost:        z.number().positive().optional(),
  paymentMethod:     z.enum(paymentMethods).optional(),
  isReporterVictim:  z.boolean().default(true),
  victimRelation:    z.string().max(100).optional(),
  victimAgeGroup:    z.enum(ageGroupOptions).optional(),
  informationAccurate: z.literal(true),     // must be checked
  consentToContact:  z.boolean().default(false),
  files:             z.array(z.custom<File>()).max(5).optional()
}).superRefine((val, ctx) => {
  if (val.scamType === "other" && !val.otherScamType)
    ctx.addIssue({code:"custom", path:["otherScamType"], message:"Please describe the scam type"});
  if (val.moneyLost && (val.amountLost==null || val.paymentMethod==null))
    ctx.addIssue({code:"custom", message:"Amount and method are required when money was lost"});
});

// ---- 2.  React component ----
export default function ReportScamForm() {
  const form = useForm<z.infer<typeof reportSchema>>({
    resolver: zodResolver(reportSchema),
    defaultValues: { moneyLost:false, isReporterVictim:true }
  });

  const onSubmit = async (values: z.infer<typeof reportSchema>) => {
    const fd = new FormData();
    Object.entries(values).forEach(([k,v]) => {
      if (k === "files") return;
      if (v !== undefined) fd.append(k, String(v));
    });
    values.files?.forEach(f => fd.append("evidence_files", f));

    try {
      await axios.post("/api/reports", fd, { headers:{ "Content-Type":"multipart/form-data" }});
      toast.success("Report submitted. Thank you for helping us fight scams!");
      form.reset();
    } catch (err:any) {
      toast.error(err.response?.data?.detail ?? "Upload failed");
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Reporter Information */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="reporterName"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Name (Optional)</FormLabel>
                <FormControl>
                  <Input placeholder="Enter your name" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name="reporterEmail"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email Address</FormLabel>
                <FormControl>
                  <Input type="email" placeholder="Enter your email" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          
          <FormField
            control={form.control}
            name="reporterPhone"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Phone Number (Optional)</FormLabel>
                <FormControl>
                  <Input placeholder="Enter your phone" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        {/* Scam Details */}
        <FormField
          control={form.control}
          name="incidentDate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Date of the Incident</FormLabel>
              <FormControl>
                <Input type="date" {...field} value={field.value.toISOString().split('T')[0]} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="scamType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Type of Scam</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select scam type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="phishing">Phishing email/text</SelectItem>
                  <SelectItem value="fake_website">Fake website</SelectItem>
                  <SelectItem value="investment">Investment scam</SelectItem>
                  <SelectItem value="tech_support">Tech support scam</SelectItem>
                  <SelectItem value="romance">Romance scam</SelectItem>
                  <SelectItem value="job">Job scam</SelectItem>
                  <SelectItem value="impersonation">Impersonation</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Brief Description</FormLabel>
              <FormControl>
                <Textarea 
                  placeholder="Describe what happened..."
                  className="min-h-[100px]"
                  {...field} 
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Consent Checkbox */}
        <FormField
          control={form.control}
          name="informationAccurate"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
              <FormControl>
                <Checkbox
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>
                  I confirm that the information provided is accurate to the best of my knowledge.
                </FormLabel>
              </div>
            </FormItem>
          )}
        />

        <Button type="submit" className="w-full">
          Submit Report
        </Button>
      </form>
    </Form>
  );
}