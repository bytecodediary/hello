"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import type { ComponentType } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

interface AuthUser {
  username: string;
  email: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  error: string | null;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
}

// Create context with default values
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const getStoredUser = (): AuthUser | null => {
  if (typeof window === "undefined") {
    return null;
  }
  const storedUser = window.localStorage.getItem("user");
  return storedUser ? (JSON.parse(storedUser) as AuthUser) : null;
};

const getStoredToken = (): string | null => {
  if (typeof window === "undefined") {
    return null;
  }
  return window.localStorage.getItem("token");
};

export const AuthProvider = ({ children }: { children: ReactNode }): JSX.Element => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const isMounted = useRef(false);

  const hydrateFromStorage = useCallback((): { token: string | null } => {
    if (typeof window === "undefined") {
      return { token: null };
    }

    const storedUser = getStoredUser();
    if (storedUser) {
      setUser(storedUser);
    }

    const token = getStoredToken();
    return { token };
  }, []);

  const performCheck = useCallback(
    async (tokenOverride?: string | null): Promise<void> => {
      if (typeof window === "undefined") return;

      const token = tokenOverride ?? getStoredToken();

      if (!token) {
        window.localStorage.removeItem("user");
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const res = await fetch(`${API_BASE_URL}/user/check_authentication/`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          credentials: "include",
        });

        if (!res.ok) {
          throw new Error(`Auth check failed with status: ${res.status}`);
        }

        const data = await res.json();
        if (data.authenticated) {
          const userInfo: AuthUser = {
            username: data.username,
            email: data.email,
          };
          window.localStorage.setItem("user", JSON.stringify(userInfo));
          setUser(userInfo);
        } else {
          window.localStorage.removeItem("user");
          setUser(null);
        }
      } catch (err) {
        console.error("Authentication check failed:", err);
        const message = err instanceof Error ? err.message : "Authentication check failed";
        setError(message);
        setUser(null);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    if (isMounted.current) return;
    isMounted.current = true;

    const { token } = hydrateFromStorage();
    void performCheck(token);
  }, [hydrateFromStorage, performCheck]);

  const logout = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);

      const token = getStoredToken();

      await fetch(`${API_BASE_URL}/user/logout/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout failed:", err);
      const message = err instanceof Error ? err.message : "Logout failed";
      setError(message);
    } finally {
      if (typeof window !== "undefined") {
        window.localStorage.removeItem("token");
        window.localStorage.removeItem("user");
      }
      setUser(null);
      setLoading(false);
    }
  };

  const refreshAuth = async (): Promise<void> => {
    await performCheck();
  };

  const value: AuthContextValue = {
    user,
    loading,
    error,
    logout,
    refreshAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const withAuth = <P extends Record<string, unknown>>(WrappedComponent: ComponentType<P>) => {
  const ComponentWithAuth = (props: P) => {
    const { loading, error } = useAuth();

    if (loading) {
      return <div>Loading...</div>;
    }

    if (error) {
      return <div>Error: {error}</div>;
    }

    return <WrappedComponent {...props} />;
  };

  ComponentWithAuth.displayName = `WithAuth(${WrappedComponent.displayName ?? WrappedComponent.name ?? "Component"})`;

  return ComponentWithAuth;
};