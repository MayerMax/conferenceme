import { TestBed, inject } from '@angular/core/testing';

import { StoreConferencesService } from './store-conferences.service';

describe('StoreConferencesService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StoreConferencesService]
    });
  });

  it('should be created', inject([StoreConferencesService], (service: StoreConferencesService) => {
    expect(service).toBeTruthy();
  }));
});
