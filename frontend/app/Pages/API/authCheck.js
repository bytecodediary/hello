import React, { createContext, useContext, useEffect, useState } from 'react';

// Create context with default values
const AuthContext = createContext({
  user: null,
  loading: true,
  error: null,
  logout: () => {},
});

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                // Reset error state at the start of each check
                setError(null);
                
                const res = await fetch('/user/check_authentication/', {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include', // Important for cookies
                });

                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }

                const data = await res.json();
                
                if (data.authenticated) {
                    setUser(data.username);
                } else {
                    setUser(null);
                }
            } catch (err) {
                console.error('Authentication check failed:', err);
                setError(err.message);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();

        // Cleanup function
        return () => {
            // Cancel any pending requests if needed
        };
    }, []);

    const logout = async () => {
        try {
            setLoading(true);
            setError(null);

            const res = await fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });

            if (!res.ok) {
                throw new Error(`Logout failed with status: ${res.status}`);
            }

            setUser(null);
        } catch (err) {
            console.error('Logout failed:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // Refresh auth function
    const refreshAuth = async () => {
        const checkAuth = async () => {
            setLoading(true);
            try {
                const res = await fetch('/user/check_authentication/');
                const data = await res.json();
                if (data.authenticated) {
                    setUser(data.username);
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        await checkAuth();
    };

    const value = {
        user,
        loading,
        error,
        logout,
        refreshAuth,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom hook with error handling
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Example usage with error boundaries
export const withAuth = (WrappedComponent) => {
    return function WithAuthComponent(props) {
        const { loading, error } = useAuth();

        if (loading) {
            return <div>Loading...</div>;
        }

        if (error) {
            return <div>Error: {error}</div>;
        }

        return <WrappedComponent {...props} />;
    };
};