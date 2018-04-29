import { TestBed, inject } from '@angular/core/testing';

import { CanDeactiveGuardService } from './can-deactive-guard.service';

describe('CanDeactiveGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CanDeactiveGuardService]
    });
  });

  it('should be created', inject([CanDeactiveGuardService], (service: CanDeactiveGuardService) => {
    expect(service).toBeTruthy();
  }));
});
