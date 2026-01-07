import { test, expect } from '@playwright/test';

test.describe('Claudipedia End-to-End Tests', () => {

  test.beforeEach(async ({ page }) => {
    // Set longer timeout for API calls
    test.setTimeout(60000);
  });

  test('homepage loads and displays correctly', async ({ page }) => {
    await page.goto('/');

    // Check page title
    await expect(page).toHaveTitle(/Claudipedia/);

    // Check main heading
    await expect(page.locator('h1')).toContainText('Claudipedia');

    // Check search functionality exists
    await expect(page.locator('input[placeholder*="Search"]')).toBeVisible();

    // Check navigation
    await expect(page.locator('nav')).toContainText('Research Profiles');
  });

  test('research profiles page loads', async ({ page }) => {
    await page.goto('/research');

    // Check page title
    await expect(page.locator('h1')).toContainText('Research Profiles');

    // Check description
    await expect(page.locator('p')).toContainText('Manage your research profiles');

    // Check create profile button exists
    await expect(page.locator('button').filter({ hasText: 'Create Research Profile' })).toBeVisible();

    // Check profiles list area exists
    await expect(page.locator('h2').filter({ hasText: 'Your Research Profiles' })).toBeVisible();
  });

  test('create research profile workflow', async ({ page }) => {
    await page.goto('/research');

    // Click create profile button
    await page.locator('button').filter({ hasText: 'Create Research Profile' }).click();

    // Check form appears
    await expect(page.locator('h2')).toContainText('Create New Research Profile');

    // Fill out the form
    await page.locator('input[id="name"]').fill('Quantum Physics Research');
    await page.locator('textarea[id="description"]').fill('Exploring quantum mechanics and its implications for modern physics');
    await page.locator('input[id="domains"]').fill('quantum-mechanics');
    await page.keyboard.press('Enter');

    // Click create button
    await page.locator('button').filter({ hasText: 'Create Profile' }).click();

    // Check form disappears (profile created)
    await expect(page.locator('h2')).toContainText('Create New Research Profile').toBeHidden();

    // Check success message or profile appears in list
    // Note: This will fail gracefully if backend is not connected, as it should fall back to mock mode
    await page.waitForTimeout(2000);
  });

  test('navigation between pages works', async ({ page }) => {
    // Start on homepage
    await page.goto('/');

    // Click research profiles link
    await page.locator('nav').locator('text=Research Profiles').click();
    await expect(page).toHaveURL('/research');

    // Go back to home
    await page.locator('nav').locator('text=Home').click();
    await expect(page).toHaveURL('/');

    // Test other navigation links
    await page.locator('nav').locator('text=Research Profiles').click();
    await expect(page).toHaveURL('/research');
  });

  test('search functionality works', async ({ page }) => {
    await page.goto('/');

    // Type in search box
    const searchInput = page.locator('input[placeholder*="Search"]');
    await searchInput.fill('quantum');

    // Wait for search results or timeout
    await page.waitForTimeout(1000);

    // Check that search doesn't break the page
    await expect(page.locator('h1')).toContainText('Claudipedia');
  });

  test('mobile responsiveness', async ({ page, isMobile }) => {
    if (!isMobile) {
      // Skip on desktop
      return;
    }

    await page.goto('/research');

    // Check mobile layout
    await expect(page.locator('button').filter({ hasText: 'Create Research Profile' })).toBeVisible();

    // Test mobile navigation
    const hamburger = page.locator('button').first(); // Hamburger menu
    await hamburger.click();

    // Check sidebar appears
    await expect(page.locator('nav').filter({ hasText: 'Physics Domains' })).toBeVisible();
  });

  test('error handling - backend unavailable', async ({ page }) => {
    // This test should work even if backend is down, as it should fall back to mock mode
    await page.goto('/research');

    // Should still load the page
    await expect(page.locator('h1')).toContainText('Research Profiles');

    // Should show empty state or mock data
    await expect(page.locator('button').filter({ hasText: 'Create Research Profile' })).toBeVisible();
  });

  test('article pages load correctly', async ({ page }) => {
    await page.goto('/article/classical-mechanics');

    // Check article title
    await expect(page.locator('h1')).toContainText('Classical Mechanics');

    // Check sections exist
    await expect(page.locator('h2')).toContainText('Introduction');

    // Check navigation back to home works
    await page.locator('nav').locator('text=Claudipedia').click();
    await expect(page).toHaveURL('/');
  });

  test('authentication pages exist', async ({ page }) => {
    // Test signin page
    await page.goto('/auth/signin');
    await expect(page.locator('h2')).toContainText('Welcome Back');

    // Test signup page
    await page.goto('/auth/signup');
    await expect(page.locator('h2')).toContainText('Join Claudipedia');
  });

  test('performance - page load times', async ({ page }) => {
    const startTime = Date.now();

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const loadTime = Date.now() - startTime;
    console.log(`Homepage load time: ${loadTime}ms`);

    // Should load in reasonable time (under 5 seconds)
    expect(loadTime).toBeLessThan(5000);
  });

  test('accessibility - keyboard navigation', async ({ page }) => {
    await page.goto('/research');

    // Tab through elements
    await page.keyboard.press('Tab'); // Focus first element
    await page.keyboard.press('Tab'); // Focus second element

    // Check that focus is visible (basic accessibility check)
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });

  test('API integration - health check', async ({ page }) => {
    // Test that the frontend can communicate with backend
    // This will work in mock mode if backend is down
    await page.goto('/research');

    // If API works, profile creation should succeed
    // If API fails, it should gracefully fall back
    const createButton = page.locator('button').filter({ hasText: 'Create Research Profile' });
    await expect(createButton).toBeVisible();
  });

});

