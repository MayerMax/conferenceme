import { TestBed, inject } from '@angular/core/testing';

import { MockGetDataService } from './mock-get-data.service';

describe('MockGetDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MockGetDataService]
    });
  });

  it('should be created', inject([MockGetDataService], (service: MockGetDataService) => {
    expect(service).toBeTruthy();
  }));
});
